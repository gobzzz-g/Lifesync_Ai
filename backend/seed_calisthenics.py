import sys
import os

# Add backend dir to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.fitness import Exercise, Base

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_exercises():
    db = SessionLocal()
    
    # We don't want to delete existing exercises unless they're duplicates, 
    # but since this is a new comprehensive list, we can just check if "Wall Push-up" exists.
    exists = db.query(Exercise).filter(Exercise.name == "Wall Push-up").first()
    if exists:
        print("Calisthenics exercises already seeded.")
        return

    exercises = [
        # --- PUSH PROGRESSIONS ---
        {
            "name": "Wall Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Chest, Triceps, Shoulders",
            "difficulty": "Beginner",
            "progression_level": 1,
            "equipment_required": "None",
            "form_setup": "Stand an arm's length from a wall, hands flat against it.",
            "form_movement": "Bend elbows to bring chest to wall, then push back.",
            "form_breathing": "Inhale on the way to the wall, exhale pushing away.",
            "common_mistakes": "Flaring elbows, losing core tension.",
            "regression": "None",
            "progression": "Incline Push-up"
        },
        {
            "name": "Incline Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Chest, Triceps, Shoulders",
            "difficulty": "Beginner",
            "progression_level": 2,
            "equipment_required": "Bench or Chair",
            "form_setup": "Hands on elevated surface, body in a straight line.",
            "form_movement": "Lower chest to edge of surface, push back up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Sagging hips.",
            "regression": "Wall Push-up",
            "progression": "Knee Push-up"
        },
        {
            "name": "Knee Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Chest, Triceps, Shoulders",
            "difficulty": "Beginner",
            "progression_level": 3,
            "equipment_required": "None",
            "form_setup": "Knees on floor, hands shoulder-width apart.",
            "form_movement": "Lower body until chest is near floor, push up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Leaving hips behind (butt in air).",
            "regression": "Incline Push-up",
            "progression": "Standard Push-up"
        },
        {
            "name": "Standard Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Chest, Triceps, Shoulders, Core",
            "difficulty": "Intermediate",
            "progression_level": 4,
            "equipment_required": "None",
            "form_setup": "High plank position, body in a straight line.",
            "form_movement": "Lower until chest is 1 inch from floor, push up fully.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Sagging hips, elbows flared at 90 degrees.",
            "regression": "Knee Push-up",
            "progression": "Diamond Push-up"
        },
        {
            "name": "Diamond Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Triceps, Inner Chest",
            "difficulty": "Intermediate",
            "progression_level": 5,
            "equipment_required": "None",
            "form_setup": "Hands together forming a diamond shape.",
            "form_movement": "Lower chest to hands, push back up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Elbows completely flared out.",
            "regression": "Standard Push-up",
            "progression": "Decline Push-up"
        },
        {
            "name": "Decline Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Upper Chest, Shoulders, Triceps",
            "difficulty": "Intermediate",
            "progression_level": 6,
            "equipment_required": "Bench or Chair",
            "form_setup": "Feet elevated, hands on floor.",
            "form_movement": "Lower chest to floor, push back up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Sagging lower back.",
            "regression": "Diamond Push-up",
            "progression": "Archer Push-up"
        },
        {
            "name": "Archer Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Chest, Shoulders, Triceps",
            "difficulty": "Advanced",
            "progression_level": 7,
            "equipment_required": "None",
            "form_setup": "Hands wider than shoulder-width, fingers pointing outward.",
            "form_movement": "Lower to one side, keeping other arm straight. Push back up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Bending the straight arm.",
            "regression": "Decline Push-up",
            "progression": "Pseudo Planche Push-up"
        },
        {
            "name": "Pseudo Planche Push-up",
            "exercise_type": "Strength",
            "muscle_groups": "Shoulders, Chest",
            "difficulty": "Advanced",
            "progression_level": 8,
            "equipment_required": "None",
            "form_setup": "Hands near hips, leaning forward.",
            "form_movement": "Lower body while maintaining forward lean, push up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Losing the forward lean during the push.",
            "regression": "Archer Push-up",
            "progression": "None"
        },
        
        # --- PULL PROGRESSIONS ---
        {
            "name": "Dead Hang",
            "exercise_type": "Strength",
            "muscle_groups": "Forearms, Grip",
            "difficulty": "Beginner",
            "progression_level": 1,
            "equipment_required": "Pull-up bar",
            "form_setup": "Grab bar with overhand grip.",
            "form_movement": "Hang passively, relaxing shoulders.",
            "form_breathing": "Breathe normally.",
            "common_mistakes": "Holding breath.",
            "regression": "None",
            "progression": "Scapular Pull-up"
        },
        {
            "name": "Scapular Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Back, Shoulders",
            "difficulty": "Beginner",
            "progression_level": 2,
            "equipment_required": "Pull-up bar",
            "form_setup": "Dead hang position.",
            "form_movement": "Pull shoulder blades down and together without bending elbows.",
            "form_breathing": "Inhale on the pull, exhale on the release.",
            "common_mistakes": "Bending elbows to cheat.",
            "regression": "Dead Hang",
            "progression": "Assisted Pull-up"
        },
        {
            "name": "Assisted Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Lats, Biceps",
            "difficulty": "Beginner",
            "progression_level": 3,
            "equipment_required": "Pull-up bar, Resistance Band",
            "form_setup": "Loop band around bar and foot/knee.",
            "form_movement": "Pull chin over bar, lower with control.",
            "form_breathing": "Exhale up, inhale down.",
            "common_mistakes": "Kicking or swinging.",
            "regression": "Scapular Pull-up",
            "progression": "Negative Pull-up"
        },
        {
            "name": "Negative Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Lats, Biceps",
            "difficulty": "Beginner",
            "progression_level": 4,
            "equipment_required": "Pull-up bar",
            "form_setup": "Jump or step up so chin is over bar.",
            "form_movement": "Slowly lower yourself over 3-5 seconds.",
            "form_breathing": "Hold at top, exhale on the way down.",
            "common_mistakes": "Dropping too fast.",
            "regression": "Assisted Pull-up",
            "progression": "Pull-up"
        },
        {
            "name": "Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Lats, Biceps, Core",
            "difficulty": "Intermediate",
            "progression_level": 5,
            "equipment_required": "Pull-up bar",
            "form_setup": "Overhand grip, slightly wider than shoulder width.",
            "form_movement": "Pull chin over bar, lower to dead hang.",
            "form_breathing": "Exhale up, inhale down.",
            "common_mistakes": "Not using full range of motion, kipping.",
            "regression": "Negative Pull-up",
            "progression": "Chin-up"
        },
        {
            "name": "Chin-up",
            "exercise_type": "Strength",
            "muscle_groups": "Biceps, Lats",
            "difficulty": "Intermediate",
            "progression_level": 6,
            "equipment_required": "Pull-up bar",
            "form_setup": "Underhand grip, shoulder-width.",
            "form_movement": "Pull chin over bar, lower fully.",
            "form_breathing": "Exhale up, inhale down.",
            "common_mistakes": "Rounding shoulders at the top.",
            "regression": "Pull-up",
            "progression": "Archer Pull-up"
        },
        {
            "name": "Archer Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Lats, Biceps",
            "difficulty": "Advanced",
            "progression_level": 7,
            "equipment_required": "Pull-up bar",
            "form_setup": "Wide grip on the bar.",
            "form_movement": "Pull body to one hand while keeping the other arm straight.",
            "form_breathing": "Exhale up, inhale down.",
            "common_mistakes": "Bending the straight arm.",
            "regression": "Chin-up",
            "progression": "Explosive Pull-up"
        },
        
        # --- MUSCLE-UP PROGRESSIONS ---
        {
            "name": "Explosive Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Lats, Biceps, Core",
            "difficulty": "Advanced",
            "progression_level": 8,
            "equipment_required": "Pull-up bar",
            "form_setup": "Standard pull-up grip.",
            "form_movement": "Pull as fast and high as possible, aiming for chest to bar.",
            "form_breathing": "Exhale explosively.",
            "common_mistakes": "Pulling slowly.",
            "regression": "Archer Pull-up",
            "progression": "Chest-to-Bar Pull-up"
        },
        {
            "name": "Chest-to-Bar Pull-up",
            "exercise_type": "Strength",
            "muscle_groups": "Lats, Upper Back",
            "difficulty": "Advanced",
            "progression_level": 9,
            "equipment_required": "Pull-up bar",
            "form_setup": "Standard grip.",
            "form_movement": "Pull aggressively until chest touches the bar.",
            "form_breathing": "Exhale pulling.",
            "common_mistakes": "Leaning too far back.",
            "regression": "Explosive Pull-up",
            "progression": "Band-Assisted Muscle-up"
        },
        {
            "name": "Muscle-up",
            "exercise_type": "Strength",
            "muscle_groups": "Back, Shoulders, Chest, Triceps",
            "difficulty": "Advanced",
            "progression_level": 11,
            "equipment_required": "Pull-up bar",
            "form_setup": "False grip or strong standard grip.",
            "form_movement": "Explosive pull-up, transition over the bar, finish with a dip.",
            "form_breathing": "Exhale on pull and dip.",
            "common_mistakes": "Chicken-winging (one arm at a time).",
            "regression": "Band-Assisted Muscle-up",
            "progression": "None"
        },

        # --- DIP PROGRESSIONS ---
        {
            "name": "Bench Dip",
            "exercise_type": "Strength",
            "muscle_groups": "Triceps",
            "difficulty": "Beginner",
            "progression_level": 1,
            "equipment_required": "Bench",
            "form_setup": "Hands behind you on a bench, legs extended.",
            "form_movement": "Lower until elbows are 90 degrees, push up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Shoulders rolling forward.",
            "regression": "None",
            "progression": "Assisted Dip"
        },
        {
            "name": "Parallel Bar Dip",
            "exercise_type": "Strength",
            "muscle_groups": "Chest, Triceps, Shoulders",
            "difficulty": "Intermediate",
            "progression_level": 3,
            "equipment_required": "Parallel Bars",
            "form_setup": "Support hold on parallel bars.",
            "form_movement": "Lower until shoulders are below elbows, push back up.",
            "form_breathing": "Inhale down, exhale up.",
            "common_mistakes": "Shrugging shoulders.",
            "regression": "Assisted Dip",
            "progression": "Weighted Dip"
        },

        # --- HANDSTAND PROGRESSIONS ---
        {
            "name": "Wall Handstand",
            "exercise_type": "Strength",
            "muscle_groups": "Shoulders, Core",
            "difficulty": "Intermediate",
            "progression_level": 1,
            "equipment_required": "Wall",
            "form_setup": "Kick up or walk feet up wall.",
            "form_movement": "Hold the position, pushing tall through shoulders.",
            "form_breathing": "Breathe normally.",
            "common_mistakes": "Banana back (excessive arch).",
            "regression": "None",
            "progression": "Wall Shoulder Taps"
        },
        {
            "name": "Freestanding Handstand",
            "exercise_type": "Balance",
            "muscle_groups": "Shoulders, Core",
            "difficulty": "Advanced",
            "progression_level": 3,
            "equipment_required": "None",
            "form_setup": "Kick up on the floor.",
            "form_movement": "Balance using fingers.",
            "form_breathing": "Breathe calmly.",
            "common_mistakes": "Looking too far back.",
            "regression": "Wall Shoulder Taps",
            "progression": "None"
        },

        # --- BALANCE/MOBILITY ---
        {
            "name": "Crow Stand",
            "exercise_type": "Balance",
            "muscle_groups": "Wrists, Shoulders, Core",
            "difficulty": "Intermediate",
            "progression_level": 1,
            "equipment_required": "None",
            "form_setup": "Squat down, place hands on floor, knees on triceps.",
            "form_movement": "Lean forward until feet leave the ground.",
            "form_breathing": "Breathe normally.",
            "common_mistakes": "Looking down instead of slightly forward.",
            "regression": "None",
            "progression": "Tuck Planche"
        },
        {
            "name": "Single-leg Balance",
            "exercise_type": "Mobility",
            "muscle_groups": "Legs, Core",
            "difficulty": "Beginner",
            "progression_level": 1,
            "equipment_required": "None",
            "form_setup": "Stand tall.",
            "form_movement": "Lift one knee up, hold balance.",
            "form_breathing": "Breathe normally.",
            "common_mistakes": "Letting hips drop.",
            "regression": "None",
            "progression": "Single-leg Reach"
        }
    ]

    for ex_data in exercises:
        ex = Exercise(**ex_data)
        db.add(ex)
    
    db.commit()
    print(f"Seeded {len(exercises)} advanced calisthenics exercises.")
    db.close()

if __name__ == "__main__":
    seed_exercises()
