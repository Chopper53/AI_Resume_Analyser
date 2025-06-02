from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import json

# Create the base class for declarative models
Base = declarative_base()

# Define the Resume model
class Resume(Base):
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    job_role = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Define the Analysis model
class Analysis(Base):
    __tablename__ = 'analyses'
    
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    analysis_data = Column(Text)  # Store JSON data
    created_at = Column(DateTime, default=datetime.datetime.utcnow)



class DatabaseManager:
    def __init__(self, db_path='resume_data.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def save_resume(self, user_id, job_role, content):
        resume = Resume(
            user_id=user_id,
            job_role=job_role,
            content=content
        )
        self.session.add(resume)
        self.session.commit()
        return resume.id
    
    def get_resume(self, resume_id):
        return self.session.query(Resume).filter(Resume.id == resume_id).first()
    
    def get_user_resumes(self, user_id):
        return self.session.query(Resume).filter(Resume.user_id == user_id).all()
    
    def save_analysis(self, resume_id, analysis_data):
        analysis = Analysis(
            resume_id=resume_id,
            analysis_data=analysis_data
        )
        self.session.add(analysis)
        self.session.commit()
        return analysis.id
    
    def get_analysis(self, analysis_id):
        return self.session.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    def get_resume_analyses(self, resume_id):
        return self.session.query(Analysis).filter(Analysis.resume_id == resume_id).all()
    
    def close(self):
        self.session.close()

def get_database_connection():
    """Get a connection to the database"""
    engine = create_engine('sqlite:///resume_data.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def save_resume_data(resume_data):
    """Save resume data to the database"""
    session = get_database_connection()
    try:
        # Convert resume_data to JSON string
        resume_json = json.dumps(resume_data)
        
        # Create a new Resume object
        resume = Resume(
            user_id="anonymous",  # We don't have user authentication yet
            job_role=resume_data.get('target_role', 'Unknown'),
            content=resume_json
        )
        
        session.add(resume)
        session.commit()
        return resume.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def save_ai_analysis_data(resume_id, analysis_data):
    """Save AI analysis data to the database"""
    session = get_database_connection()
    try:
        # Create a new AIAnalysis object
        ai_analysis = AIAnalysis(
            resume_id=resume_id,
            model_used=analysis_data.get('model_used', 'Unknown'),
            resume_score=analysis_data.get('resume_score', 0),
            job_role=analysis_data.get('job_role', 'Unknown')
        )
        
        session.add(ai_analysis)
        session.commit()
        return ai_analysis.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
