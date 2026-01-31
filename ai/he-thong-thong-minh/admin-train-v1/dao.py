import psycopg2
import psycopg2.extras # For dictionary cursor
from typing import List
from models import Sample, TrainingSample, TrainedModel # Import data classes

# --- Data Access Objects (DAO) (from UML Class Diagram) ---
# These classes are responsible for database interactions.

class Dao:
    def __init__(self, db_host: str = "localhost", 
                db_name: str = "httm", 
                db_user: str = "postgres", 
                db_pass: str = "quangphu", 
                db_port: int = 5432):
        try:
            # Establish PostgreSQL connection
            self.con = psycopg2.connect(
                host=db_host,
                dbname=db_name,
                user=db_user,
                password=db_pass,
                port=db_port
            )
            print(f"Connected to PostgreSQL database '{db_name}' at {db_host}:{db_port}")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            self.con = None

    def __del__(self):
        if self.con:
            self.con.close()
            print("PostgreSQL connection closed.")

class SampleDao(Dao):
    
    def get_list_sample(self) -> List[Sample]:
        if not self.con:
            print("No database connection.")
            return []
            
        samples: List[Sample] = []
        try:
            cursor = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            cursor.execute("SELECT id, image_file_path, label, x_min, y_min, x_max, y_max FROM tbl_sample")
            rows = cursor.fetchall()
            
            for row in rows:
                samples.append(Sample(
                    id=row['id'],
                    image_file_path=row['image_file_path'],
                    label=row['label'],
                    x_min=row['x_min'],
                    y_min=row['y_min'],
                    x_max=row['x_max'],
                    y_max=row['y_max']
                ))
            cursor.close()
            
        except psycopg2.Error as e:
            print(f"Error fetching samples: {e}")
            
        return samples

class TrainedModelDao(Dao):
    
    def save(self, model: TrainedModel) -> bool:
      
        if not self.con:
            print("No database connection.")
            return False

        try:
            cursor = self.con.cursor()
            
            # delete if model has been trained
            delete_train_sample = """
                DELETE FROM tbl_train_sample
                WHERE trained_model_id = (
                    SELECT t.id FROM tbl_trained_model t WHERE name = %s
                )
            """
            delete_model_sql = """
                DELETE FROM tbl_trained_model WHERE name = %s
            """

            # execute with single-element tuple (note the comma)
            cursor.execute(delete_train_sample, (model.name,))
            cursor.execute(delete_model_sql, (model.name,))


            # 1. Insert into tbl_trained_model
            # Using RETURNING id to get the new primary key
            insert_model_sql = """
            INSERT INTO tbl_trained_model (name, artifact_path, accuracy, f1, precision, recall)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            cursor.execute(insert_model_sql, (
                model.name, 
                model.artifact_path, 
                model.accuracy, 
                model.f1, 
                model.precision, 
                model.recall
            ))
            
            # Get the new model's ID
            new_model_id = cursor.fetchone()[0]
            model.id = new_model_id # Update the model object with its new ID
            
            # 2. Insert into the junction table tbl_train_sample
            if model.training_samples:
                insert_sample_links_sql = """
                INSERT INTO tbl_train_sample (trained_model_id, sample_id)
                VALUES (%s, %s)
                """
                # Create a list of tuples for executemany
                sample_links = [
                    (new_model_id, ts.sample.id) for ts in model.training_samples
                ]
                cursor.executemany(insert_sample_links_sql, sample_links)
            
            # Commit the transaction
            self.con.commit()
            cursor.close()
            print(f"Successfully saved model with ID: {new_model_id}")
            return True
            
        except psycopg2.Error as e:
            print(f"Error saving model: {e}")
            self.con.rollback() # Roll back changes on error
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.con.rollback()
            return False
