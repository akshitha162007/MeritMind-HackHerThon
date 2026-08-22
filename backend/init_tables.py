#!/usr/bin/env python3
"""Initialize database tables"""
from database import engine, Base
from models import (
    User, Session, JobDescription, Candidate, Resume, Application,
    BiasReport, IntersectionalBiasMatrix, CounterfactualSimulation,
    SilenceRankResult, EmotionBlindScore, ReverseBiasSimulation,
    SkillGraphMatch, FairnessMetric, Explanation, BiasHeatmapData,
    RecruiterOverride, FairnessAuditLog
)

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
