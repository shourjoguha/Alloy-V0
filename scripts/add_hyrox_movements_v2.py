#!/usr/bin/env python3
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def add_hyrox_movements():
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5434"),
            database=os.getenv("DATABASE_NAME", "Jacked-DB"),
            user=os.getenv("DATABASE_USER", "jacked"),
            password=os.getenv("DATABASE_PASSWORD", "jackedpass")
        )
        cursor = conn.cursor()

        cursor.execute("BEGIN")

        movements = [
            ('Burpee Broad Jumps', 'crossfit', 'conditioning', 'full body', 'quadriceps', True, False, False, False, False, False, False),
            ('Calorie Ski Erg', 'cardio', 'conditioning', 'full body', 'full_body', False, False, False, False, True, False, False),
            ('V-Ups', 'resistance training', 'core', 'core', 'core', True, False, False, False, False, False, False),
            ('Sit-Ups', 'resistance training', 'core', 'core', 'core', True, False, False, False, False, False, False),
            ('Sandbag Lunges', 'resistance training', 'lunge', 'lower body', 'quadriceps', False, False, False, False, False, False, True),
            ('Lunges', 'resistance training', 'lunge', 'lower body', 'quadriceps', True, False, False, False, False, False, False),
        ]

        for movement in movements:
            cursor.execute("""
                INSERT INTO movements (name, discipline, pattern, primary_region, primary_muscle,
                                      bodyweight_possible, dumbbell_possible, kettlebell_possible,
                                      barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name
            """, movement)
            result = cursor.fetchone()
            print(f"Created movement: {result[1]} (ID: {result[0]})")

        conn.commit()
        print("\nMigration executed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_hyrox_movements()
