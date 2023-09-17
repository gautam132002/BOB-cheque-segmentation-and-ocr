# Cheque Automation Python Script

This Python script automates the process of extracting important information from a scanned or photographed cheque using Azure OCR. It takes an image of a cheque as input and generates a CSV file containing the following segmented parameters: account number, date, cheque number, amount, payee, and IFSC code.

## Prerequisites

Before running the script, make sure you have the following prerequisites:

- Python 3.x installed on your system.
- Azure OCR API credentials (subscription key and endpoint). You can obtain these by signing up for Azure OCR services.
- Required Python libraries mentioned in the `requirements.txt` file. You can install them using pip.

## Usage

To run the script, follow these steps:

1. Clone or download this repository.

```bash
git clone https://github.com/your-username/BOB-cheque-segmentation-ocr.git
cd BOB-cheque-segmentation-ocr
```

2. Open `main.py` and set your Azure OCR API credentials in the `azure_ocr_config` section.

```python
subscription_key = "ADD_API_KEY OVER_HERE."
endpoint = "https://computervisionbankofbaroda.cognitiveservices.azure.com/"
```

3. Run the script using the following command:

```bash
python main.py
```

4. Provide the path to the cheque image when prompted.

5. The script will process the image, extract the required information, and generate a CSV file named `cheque_data.csv` containing the segmented parameters.

## Note

Please note that this script does not currently include signature verification. A future version (version_2) will include this feature.

## Contributions and Rules

Contributions to this repository are welcome. If you'd like to contribute, please follow these rules:

1. Fork the repository and create a feature branch for your contribution.
2. Make your changes and ensure the code remains well-documented and adheres to PEP 8 coding standards.
3. Create a pull request describing your changes and their purpose.

## Colab Notebook
[Colab Notebook](https://colab.research.google.com/drive/1VDx07_yg-4H4YsalQjkvoD0Q-1YFoLB8?usp=sharing#scrollTo=Smv1n1mZ3YTD)
