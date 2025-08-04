import os
import json
import matplotlib.pyplot as plt

json_file_path = "file path" 

if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    print("components:", len(data["reports"]))
    print("vulnerable:", len(data["vulnerable"]))
    total_components = len(data["reports"])
    vulnerable_components = len(data["vulnerable"])
    non_vulnerable = total_components - vulnerable_components

    #vulnerable
    categories = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
    for key, value in data["vulnerable"].items():
        for vulnerability in value.get("vulnerabilities", []):
            score = vulnerability.get("cvssScore", 0)
            if 0.1 <= score <= 3.9:
                categories["Low"] += 1
            elif 4.0 <= score <= 6.9:
                categories["Medium"] += 1
            elif 7.0 <= score <= 8.9:
                categories["High"] += 1
            elif 9.0 <= score <= 10.0:
                categories["Critical"] += 1
    total_threats = sum(categories.values())
    print("LOW:", categories["Low"], "MEDIUM:", categories["Medium"], "HIGH:", categories["High"], "CRITICAL:", categories["Critical"], "TOTAL:", total_threats)

    # Values and labels for total components chart
    values_total = [vulnerable_components, non_vulnerable]
    labels_total = [f'Vulnerable ({vulnerable_components})', f'Non vulnerable ({non_vulnerable})']
    colors_total = ['red', 'lightgrey']

    # Values and labels for vulnerability categories chart
    values_categories = list(categories.values())
    labels_categories = [f'{k} ({v})' for k, v in categories.items()]
    colors_categories = ["blue","yellow", "orange", "red"]

   # Create the donut charts side by side
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Total components chart
    axes[0].pie(
        values_total,
        labels=labels_total,
        startangle=90,
        colors=colors_total,
        wedgeprops=dict(width=0.6)
    )
    axes[0].set_title("Components")

    # Vulnerability categories chart
    axes[1].pie(
        values_categories,
        labels=labels_categories,
        startangle=90,
        colors=colors_categories,
        wedgeprops=dict(width=0.6)
    )
    axes[1].set_title("Threats")

    # Add descriptions below the charts
    def toPercentage(item, total):
        return f"{(item / total)* 100:.1f}%"

    # description = f"""
    # Components: {total_components}
    # - Vulnerable: {toPercentage(vulnerable_components, total_components)}
    # - Non-Vulnerable: {toPercentage(non_vulnerable, total_components)}

    # Total threats: {total_threats}
    # - Low: {toPercentage(categories['Low'], total_threats)}         
    # - Medium: {toPercentage(categories["Medium"], total_threats)}
    # - High: {toPercentage(categories["High"], total_threats)}
    # - Critical: {toPercentage(categories["Critical"], total_threats)}
    # """
    # plt.figtext(0, 0.01, description, ha="left", fontsize=9.8)

    # Display the charts
    plt.tight_layout()
    plt.show()

else:
    print(f"The file does not exist.")