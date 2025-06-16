# Fetch and parse Matter XML files.

from langchain_core.documents import Document
import xml.etree.ElementTree as ET
import requests

matter_data_model_xml_dir = "https://api.github.com/repos/project-chip/connectedhomeip/contents/data_model/master"
matter_device_type_xml_dir = f"{matter_data_model_xml_dir}/device_types"
matter_cluster_xml_dir = f"{matter_data_model_xml_dir}/clusters"

MATTER_XML_COLLECTION_NAME = "matter_xmls"

def get_xml_files_from_url(repo_url):
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        xml_files = [file for file in files if file["name"].endswith(".xml")]
        documents = []

        for xml_file in xml_files:
            file_url = xml_file["download_url"]
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                doc = Document(
                    page_content=file_response.text,
                    metadata={"source": xml_file["name"], "url": file_url}
                )
                documents.append(doc)
            else:
                print(f"❌ Failed to fetch file content for {xml_file['name']}: {file_response.status_code}")
        
        return documents
    else:
        print(f"❌ Failed to fetch XML files from GitHub API: {response.status_code}")
        return []


def load_and_split_matter_xmls():
    cluster_xmls = get_xml_files_from_url(matter_cluster_xml_dir)
    cluster_doc_chunks = []
    for doc in cluster_xmls:
        parsed_chunks = parse_matter_cluster_xml(doc)
        cluster_doc_chunks.extend(parsed_chunks)
    
    # summarize_doc_sizes(cluster_doc_chunks)

    device_type_xmls = get_xml_files_from_url(matter_device_type_xml_dir)
    device_type_chunks = []
    for doc in device_type_xmls:
        parsed_chunks = parse_matter_device_type_xml(doc)
        device_type_chunks.extend(parsed_chunks)
    
    # summarize_doc_sizes(device_type_chunks)

    print(f"📂 Number of Matter cluster XMLs: {len(cluster_xmls)}")
    print(f"📂 Number of Matter device type XMLs: {len(device_type_xmls)}")

    matter_xmls = cluster_xmls + device_type_xmls
    matter_doc_objects = cluster_doc_chunks + device_type_chunks

    for doc in matter_doc_objects:
        if not doc.page_content:
            print(doc)

    texts = [doc.page_content for doc in matter_doc_objects]
    textData = [
        {"source": doc.metadata.get("source", ""), "text": doc.page_content}
        for doc in matter_doc_objects
    ]

    print(f"✅ Split {len(matter_xmls)} Matter XML files into {len(textData)} document objects.")
    return texts, textData


def parse_matter_cluster_xml(document):
    """Parse a Matter cluster XML file into structured Document chunks."""
    xml_str = document.page_content
    source = document.metadata.get("source", "unknown")
    docs = []

    try:
        root = ET.fromstring(xml_str)

        # Get cluster name and IDs
        cluster_name = root.attrib.get("name", "Unknown Cluster")
        cluster_ids = [
            el.attrib.get("id", "Unknown")
            for el in root.findall("clusterIds/clusterId")
        ]
        cluster_id_str = ", ".join(cluster_ids) if cluster_ids else "Unknown"
        cluster_header = f"Cluster: {cluster_name} (ID: {cluster_id_str})\n"

        def make_doc(tag_type, content):
            return Document(
                page_content=cluster_header + f"Type: {tag_type}\n{content}",
                metadata={"type": tag_type, "cluster": cluster_name, "source": source}
            )
        
        merged_tags = ["revisionHistory", "clusterIds", "classification"]
        merged_content = ""
        for tag in merged_tags:
            el = root.find(tag)
            if el is not None:
                merged_content += ET.tostring(el, encoding="unicode")
        if merged_content:
            docs.append(make_doc("cluster metadata", merged_content.strip()))

        # Single-block XML tags that map directly to one document
        single_tags = [
            "features",
            "attributes",
            "commands",
            "events"
        ]
        for tag in single_tags:
            el = root.find(tag)
            if el is not None:
                content = ET.tostring(el, encoding="unicode")
                docs.append(make_doc(tag, content))

        # Multi-element blocks (combine into one document per type)
        multi_element_defs = {
            "enums": "dataTypes/enum",
            "structs": "dataTypes/struct",
            "bitmaps": "dataTypes/bitmap",
        }
        for tag_type, xpath in multi_element_defs.items():
            elements = root.findall(xpath)
            if elements:
                combined = "\n".join(ET.tostring(el, encoding="unicode") for el in elements)
                docs.append(make_doc(tag_type, combined))

    except ET.ParseError as e:
        print(f"❌ XML parse error in {source}: {e}")

    return docs


def parse_matter_device_type_xml(document):
    xml_str = document.page_content.strip()

    # Find start of root tag, and remove comments before it
    start = xml_str.find('<deviceType')
    if start == -1:
        return [document]
    xml_body = xml_str[start:]

    root = ET.fromstring(xml_body)
    device_type_name = root.attrib.get("name", "Unknown")
    header = f"Device Type: {device_type_name}\n"
    xml_str = header + xml_body

    return [Document(page_content=xml_str, metadata=document.metadata)]


def summarize_doc_sizes(docs):
    import statistics

    # Define ranges
    ranges = [
        (0, 500),
        (500, 1000),
        (1000, 2000),
        (2000, 5000),
        (5000, 10000),
        (10000, 20000),
        (20000, 50000),
        (50000, float('inf'))
    ]

    range_labels = [
        "0–500",
        "500–1000",
        "1000–2000",
        "2000–5000",
        "5000–10000",
        "10000–20000",
        "20000–40000",
        "40000+"
    ]

    range_counts = [0] * len(ranges)
    char_counts = []

    # Tally document sizes
    for doc in docs:
        num_chars = len(doc.page_content)
        char_counts.append(num_chars)

        for idx, (low, high) in enumerate(ranges):
            if low <= num_chars < high:
                range_counts[idx] += 1
                break

    # Summary stats
    max_chars = max(char_counts) if char_counts else 0
    avg_chars = statistics.mean(char_counts) if char_counts else 0
    median_chars = statistics.median(char_counts) if char_counts else 0

    # Print results
    print("📊 Document Character Count Summary:")
    for label, count in zip(range_labels, range_counts):
        print(f"  - {label} characters: {count} documents")

    print("\n📈 Statistics:")
    print(f"  - Max characters: {max_chars}")
    print(f"  - Average characters: {avg_chars:.2f}")
    print(f"  - Median characters: {median_chars}")

