from modules.bongo_db import BongoDB
from modules.drive_io import DriveIO
from config import PRODUCTS_SHEET_NAME, PRODUCT_HEADERS
import uuid

class ProductManager:
    def __init__(self, credentials):
        self.db = BongoDB(credentials)
        self.drive = DriveIO(credentials)
        self.products = self.db.collection(PRODUCTS_SHEET_NAME, PRODUCT_HEADERS)

    def add_product(self, name, detail, price, image_path):
        # 1. Generate PID
        pid = f"PROD-{uuid.uuid4().hex[:8]}"
        
        # 2. Upload Image to Drive (Generic folder or specific)
        try:
            # For simplicity, we reuse the root folder for product images or create a 'Products' folder
            file_id, image_url = self.drive.upload_image(image_path, self.drive.create_uid_folder("Products"))
            
            # 3. Insert into Product Collection
            self.products.insert([pid, name, detail, price, image_url])
            return True, pid
        except Exception as e:
            return False, str(e)

    def list_products(self):
        return self.products.find_all()
