import pydicom
import os


class DicomUtils(object):

    def extract_study_uid(self,input_path):
        try:
            files = [file for file in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, file))]

            for file_name in files:
                if file_name.lower().endswith('.dcm'):
                    # Construct the full path to the DICOM file
                    dicom_file_path = os.path.join(input_path, file_name)
                    # Load the DICOM file
                    dicom_data = pydicom.dcmread(dicom_file_path)

                    # Access the Study Instance UID
                    study_uid = dicom_data.StudyInstanceUID

                    return study_uid
                break
        except Exception as e:
            print(f"Error extracting Study UID: {e}")
            return None