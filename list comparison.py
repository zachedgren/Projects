import pandas as pd


def normalize_name(name):
    """Normalize name to 'Last, First' format."""
    if ',' in name:
        return name.strip().lower()
    else:
        parts = name.strip().split()
        if len(parts) == 2:
            return f"{parts[1].lower()}, {parts[0].lower()}"
        else:
            return name.strip().lower()


def compare_excel_lists(file_path, sheet_name1, column_name1, column_email1, sheet_name2, column_name2):
    # Read the Excel file
    df1 = pd.read_excel(file_path, sheet_name=sheet_name1, usecols=[column_name1, column_email1])
    df2 = pd.read_excel(file_path, sheet_name=sheet_name2, usecols=[column_name2])

    # Normalize the names from both sheets
    normalized_names1 = df1[column_name1].dropna().apply(normalize_name)
    normalized_names2 = df2[column_name2].dropna().apply(normalize_name)

    # Find the common normalized names between both sheets
    common_names = set(normalized_names1).intersection(normalized_names2)

    # Prepare lists for names and emails
    names_for_excel = []
    emails_for_excel = []

    for name, email in zip(df1[column_name1], df1[column_email1].fillna('')):
        normalized_name = normalize_name(name)
        if normalized_name in common_names:
            names_for_excel.append(name.title())  # Add the original name to the names list
            emails_for_excel.append(email if email else "")  # Add the email (empty if no email) to the email list

    # Create a DataFrame with names in one column and emails in the next
    output_df = pd.DataFrame({
        'Common Names (Last, First)': names_for_excel,
        'Email': emails_for_excel
    })

    output_file = "common_names_with_emails.xlsx"
    output_df.to_excel(output_file, index=False)

    print(f"Common names with emails saved to {output_file}")

    # Print the names and emails
    for index, row in output_df.iterrows():
        print(f"{row['Common Names (Last, First)']} - {row['Email']}")

    return output_df


# Example usage
if __name__ == "__main__":
    file_path = "Compare-lists-excel.xlsx"  # Change this to your actual file path
    sheet_name1 = "Sheet1"  # Change to your actual sheet name
    column_name1 = "My List"  # Change to the column name containing names in Sheet1
    column_email1 = "Email"  # Change to the column name containing emails in Sheet1
    sheet_name2 = "Sheet2"  # Change to your actual sheet name
    column_name2 = "SST Names"  # Change to the column name containing names in Sheet2

    common_names = compare_excel_lists(file_path, sheet_name1, column_name1, column_email1, sheet_name2, column_name2)
    print("Common Names with Emails:", common_names)
