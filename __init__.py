# -*- coding: utf-8 -*-

from . import models

def post_init_hook(env):
    try:
        env.cr.execute("""
            ALTER TABLE hr_applicant 
            ADD COLUMN IF NOT EXISTS vgr NUMERIC,
            ADD COLUMN IF NOT EXISTS ngr NUMERIC,
            ADD COLUMN IF NOT EXISTS lag NUMERIC,
            ADD COLUMN IF NOT EXISTS che NUMERIC,
            ADD COLUMN IF NOT EXISTS bei VARCHAR,
            ADD COLUMN IF NOT EXISTS vcr NUMERIC,
            ADD COLUMN IF NOT EXISTS ncr NUMERIC,
            ADD COLUMN IF NOT EXISTS recruitment_phase VARCHAR,
            ADD COLUMN IF NOT EXISTS hire_decision VARCHAR,
            ADD COLUMN IF NOT EXISTS contract_type_id INTEGER,
            ADD COLUMN IF NOT EXISTS meets_staff_requirements BOOLEAN,
            ADD COLUMN IF NOT EXISTS total_score NUMERIC
        """)
        env.cr.commit()
    except Exception as e:
        print(f"Error creating columns: {e}")