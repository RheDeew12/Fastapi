from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Model data untuk jadwal konsultasi dokter
class DoctorConsultation(BaseModel):

    id: int
    doctor_name: str
    patient_name: str
    appointment_time: str
    appointment_date: str
    description: Optional[str] = None

# In-memory database untuk menyimpan daftar jadwal konsultasi dokter
doctor_consultation_db = []

# Endpoint untuk mendapatkan daftar seluruh jadwal konsultasi dokter
@app.get("/consultations", response_model=List[DoctorConsultation])
async def get_consultations():
    """
    Get all doctor consultation schedules available in the database.
    """
    return doctor_consultation_db

# Endpoint untuk mendapatkan detail jadwal konsultasi dokter berdasarkan ID
@app.get("/consultations/{consultation_id}", response_model=DoctorConsultation)
async def get_consultation(consultation_id: int):
    """
    Get details of a doctor consultation schedule based on its ID.
    """
    for consultation in doctor_consultation_db:
        if consultation.id == consultation_id:
            return consultation
    # Jika jadwal konsultasi dokter tidak ditemukan, raise HTTPException dengan status 404
    raise HTTPException(status_code=404, detail="Consultation schedule not found")

# Endpoint untuk menambahkan jadwal konsultasi dokter baru ke dalam database
@app.post("/consultations", response_model=DoctorConsultation)
async def create_consultation(consultation: DoctorConsultation):
    """
    Create a new doctor consultation schedule entry in the database.
    """
    # Periksa apakah jadwal konsultasi dokter dengan ID yang sama sudah ada di database
    for existing_consultation in doctor_consultation_db:
        if existing_consultation.id == consultation.id:
            # Jika jadwal konsultasi dokter dengan ID yang sama sudah ada, raise HTTPException dengan status 400
            raise HTTPException(status_code=400, detail="Consultation schedule with this ID already exists")
    # Tambahkan jadwal konsultasi dokter baru ke dalam database
    doctor_consultation_db.append(consultation)
    return consultation

# Endpoint untuk memperbarui detail jadwal konsultasi dokter berdasarkan ID
@app.put("/consultations/{consultation_id}", response_model=DoctorConsultation)
async def update_consultation(consultation_id: int, updated_consultation: DoctorConsultation):
    """
    Update details of a doctor consultation schedule based on its ID.
    """
    for index, consultation in enumerate(doctor_consultation_db):
        if consultation.id == consultation_id:
            # Jika jadwal konsultasi dokter dengan ID yang sesuai ditemukan, perbarui detailnya
            doctor_consultation_db[index] = updated_consultation
            return updated_consultation
    # Jika jadwal konsultasi dokter tidak ditemukan, raise HTTPException dengan status 404
    raise HTTPException(status_code=404, detail="Consultation schedule not found")

# Endpoint untuk menghapus jadwal konsultasi dokter berdasarkan ID
@app.delete("/consultations/{consultation_id}", response_model=dict)
async def delete_consultation(consultation_id: int):
    """
    Delete a doctor consultation schedule from the database based on its ID.
    """
    for index, consultation in enumerate(doctor_consultation_db):
        if consultation.id == consultation_id:
            # Jika jadwal konsultasi dokter dengan ID yang sesuai ditemukan, hapus jadwal tersebut
            del doctor_consultation_db[index]
            return {"message": "Consultation schedule deleted"}
    # Jika jadwal konsultasi dokter tidak ditemukan, raise HTTPException dengan status 404
    raise HTTPException(status_code=404, detail="Consultation schedule not found")

# Jalankan aplikasi jika file ini dijalankan secara langsung
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)