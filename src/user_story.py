"""User Story Module for Scrum Project Management
Provides functionality to create, update, prioritize, and track user stories in the product and sprint backlogs.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class UserStoryService:
    VALID_PRIORITIES = ("Must Have", "Should Have", "Could Have", "Won't Have")
    VALID_STATUSES = ("Backlog", "To Do", "In Progress", "Review/Testing", "Done")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_user_story(
        self,
        story_code: str,
        title: str,
        role: str,
        want: str,
        benefit: str,
        priority: str = "Must Have",
        story_points: int = 3,
        sprint_id: Optional[int] = None,
        status: str = "Backlog",
        assignee: str = "",
        description: str = ""
    ) -> Dict[str, Any]:
        """Creates a new User Story following standard Agile formatting."""
        story_code = story_code.strip().upper()
        title = title.strip()
        role = role.strip()
        want = want.strip()
        benefit = benefit.strip()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {', '.join(self.VALID_PRIORITIES)}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO user_stories (
                    story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee.strip(), description.strip()))
            conn.commit()
            story_id = cursor.lastrowid
            return {
                "id": story_id,
                "story_code": story_code,
                "title": title,
                "role": role,
                "want": want,
                "benefit": benefit,
                "priority": priority,
                "story_points": story_points,
                "sprint_id": sprint_id,
                "status": status,
                "assignee": assignee,
                "description": description
            }
        except sqlite3.IntegrityError:
            raise ValueError(f"User Story with code '{story_code}' already exists.")
        finally:
            conn.close()

    def get_user_story(self, story_code: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single user story by its unique code (e.g. US-01)."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_stories WHERE UPPER(story_code) = ?;", (story_code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def list_user_stories(
        self,
        sprint_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists user stories with optional filters."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM user_stories WHERE 1=1"
        params: List[Any] = []

        if sprint_id is not None:
            query += " AND sprint_id = ?"
            params.append(sprint_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)

        query += " ORDER BY id ASC;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_status(self, story_code: str, new_status: str) -> Dict[str, Any]:
        """Transitions a user story across Kanban states."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_stories SET status = ? WHERE UPPER(story_code) = ?;
        """, (new_status, story_code.strip().upper()))
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"User Story '{story_code}' not found.")

        conn.commit()
        conn.close()
        story = self.get_user_story(story_code)
        assert story is not None
        return story
