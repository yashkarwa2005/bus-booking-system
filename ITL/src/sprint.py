"""Sprint Management Module for Scrum Framework
Handles Sprint planning, commitments, velocity tracking, and backlog allocations.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class SprintService:
    VALID_STATUSES = ("Planning", "Active", "Completed")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_sprint(
        self,
        sprint_number: int,
        name: str,
        goal: str,
        start_date: str,
        end_date: str,
        status: str = "Planning"
    ) -> Dict[str, Any]:
        """Creates a new Scrum Sprint iteration."""
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid sprint status '{status}'.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
                VALUES (?, ?, ?, ?, ?, ?, 0);
            """, (sprint_number, name.strip(), goal.strip(), start_date.strip(), end_date.strip(), status))
            conn.commit()
            sprint_id = cursor.lastrowid
            return {
                "id": sprint_id,
                "sprint_number": sprint_number,
                "name": name,
                "goal": goal,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "velocity": 0
            }
        except sqlite3.IntegrityError:
            raise ValueError(f"Sprint number {sprint_number} already exists.")
        finally:
            conn.close()

    def get_sprint(self, sprint_number: int) -> Optional[Dict[str, Any]]:
        """Retrieves details of a specific sprint."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sprints WHERE sprint_number = ?;", (sprint_number,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def list_sprints(self) -> List[Dict[str, Any]]:
        """Returns all configured sprints."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sprints ORDER BY sprint_number ASC;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_sprint_metrics(self, sprint_id: int) -> Dict[str, Any]:
        """Calculates story points, commitment, and completion rates for a sprint."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sprints WHERE id = ?;", (sprint_id,))
        sprint = cursor.fetchone()
        if not sprint:
            conn.close()
            raise ValueError(f"Sprint ID {sprint_id} not found.")

        cursor.execute("""
            SELECT
                COUNT(*) AS total_stories,
                COALESCE(SUM(story_points), 0) AS committed_points,
                COALESCE(SUM(CASE WHEN status = 'Done' THEN story_points ELSE 0 END), 0) AS completed_points
            FROM user_stories
            WHERE sprint_id = ?;
        """, (sprint_id,))
        row = cursor.fetchone()
        conn.close()

        committed = row["committed_points"]
        completed = row["completed_points"]
        completion_pct = round((completed / committed * 100), 1) if committed > 0 else 0.0

        return {
            "sprint_id": sprint["id"],
            "sprint_number": sprint["sprint_number"],
            "name": sprint["name"],
            "goal": sprint["goal"],
            "status": sprint["status"],
            "total_stories": row["total_stories"],
            "committed_points": committed,
            "completed_points": completed,
            "completion_percentage": completion_pct
        }
