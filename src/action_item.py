"""Action Items Module for Scrum Impediment & Task Management
Tracks continuous improvement tasks and impediments identified during Sprint Planning,
Daily Scrums, and Retrospectives.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class ActionItemService:
    VALID_PRIORITIES = ("High", "Medium", "Low")
    VALID_STATUSES = ("To Do", "In Progress", "Review", "Done", "Blocked")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_action_item(
        self,
        item_code: str,
        description: str,
        owner: str,
        priority: str = "High",
        due_date: str = "",
        sprint_id: Optional[int] = None,
        status: str = "To Do"
    ) -> Dict[str, Any]:
        """Creates a new actionable Scrum task."""
        item_code = item_code.strip().upper()
        description = description.strip()
        owner = owner.strip()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {', '.join(self.VALID_PRIORITIES)}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO action_items (
                    item_code, description, sprint_id, owner, priority, due_date, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (item_code, description, sprint_id, owner, priority, due_date.strip(), status))
            conn.commit()
            item_id = cursor.lastrowid
            return {
                "id": item_id,
                "item_code": item_code,
                "description": description,
                "sprint_id": sprint_id,
                "owner": owner,
                "priority": priority,
                "due_date": due_date,
                "status": status
            }
        except sqlite3.IntegrityError:
            raise ValueError(f"Action item with code '{item_code}' already exists.")
        finally:
            conn.close()

    def list_action_items(
        self,
        sprint_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists action items with optional filters."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM action_items WHERE 1=1"
        params: List[Any] = []

        if sprint_id is not None:
            query += " AND sprint_id = ?"
            params.append(sprint_id)
        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY id ASC;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_status(self, item_code: str, new_status: str) -> Dict[str, Any]:
        """Updates the status of an action item."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE action_items SET status = ? WHERE UPPER(item_code) = ?;
        """, (new_status, item_code.strip().upper()))

        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"Action item '{item_code}' not found.")

        conn.commit()
        cursor.execute("SELECT * FROM action_items WHERE UPPER(item_code) = ?;", (item_code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()
        assert row is not None
        return dict(row)
