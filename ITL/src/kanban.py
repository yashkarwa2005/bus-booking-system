"""Kanban Board Module for Agile Project Tracking
Visualizes task progression across 5 stages (Backlog -> To Do -> In Progress -> Review/Testing -> Done)
in an interactive terminal display.
"""
from typing import List, Dict, Any, Optional
from src.user_story import UserStoryService
from src.action_item import ActionItemService


class KanbanService:
    COLUMNS = ["Backlog", "To Do", "In Progress", "Review/Testing", "Done"]

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.story_service = UserStoryService(db_path)
        self.action_service = ActionItemService(db_path)

    def get_board_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups user stories and action items into the 5 Kanban columns."""
        stories = self.story_service.list_user_stories()
        actions = self.action_service.list_action_items()

        board: Dict[str, List[Dict[str, Any]]] = {col: [] for col in self.COLUMNS}

        # Map User Stories
        for s in stories:
            col = s["status"]
            if col in board:
                board[col].append({
                    "type": "STORY",
                    "code": s["story_code"],
                    "title": s["title"],
                    "priority": s["priority"],
                    "points": s["story_points"],
                    "assignee": s["assignee"] or "Unassigned"
                })

        # Map Action Items
        action_status_map = {
            "To Do": "To Do",
            "In Progress": "In Progress",
            "Review": "Review/Testing",
            "Done": "Done",
            "Blocked": "In Progress"
        }
        for a in actions:
            target_col = action_status_map.get(a["status"], "To Do")
            if target_col in board:
                board[target_col].append({
                    "type": "ACTION",
                    "code": a["item_code"],
                    "title": a["description"],
                    "priority": a["priority"],
                    "points": 1,
                    "assignee": a["owner"] or "Unassigned"
                })

        return board

    def get_priority_symbol(self, priority: str) -> str:
        """Returns colored badge or emoji representation for task priority."""
        p = priority.lower()
        if "must" in p or "high" in p:
            return "[!] High"
        elif "should" in p or "medium" in p:
            return "[-] Med"
        else:
            return "[*] Low"

    def render_terminal_board(self) -> str:
        """Renders an ASCII text-based representation of the 5-column Kanban board."""
        board = self.get_board_data()
        lines = []

        lines.append("=" * 115)
        lines.append("             BUS BOOKING SYSTEM - LIVE SCRUM KANBAN BOARD (SPRINT CADENCE)")
        lines.append("=" * 115)

        # Header with counts
        header_parts = []
        for col in self.COLUMNS:
            count = len(board[col])
            header_parts.append(f" {col.upper()} ({count})".center(22))
        lines.append("|" + "|".join(header_parts) + "|")
        lines.append("-" * 115)

        # Calculate max rows
        max_items = max(len(items) for items in board.values()) if any(board.values()) else 0

        if max_items == 0:
            lines.append("|" + " (No Items) ".center(113) + "|")
        else:
            for idx in range(max_items):
                row_cells = []
                for col in self.COLUMNS:
                    items = board[col]
                    if idx < len(items):
                        item = items[idx]
                        code = item["code"]
                        prio = self.get_priority_symbol(item["priority"])
                        pts = f"{item['points']}pt"
                        title = item["title"][:14]
                        cell_text = f"{code} {prio} {pts} {title}"
                        row_cells.append(f" {cell_text[:20]} ".ljust(22))
                    else:
                        row_cells.append(" " * 22)
                lines.append("|" + "|".join(row_cells) + "|")

        lines.append("=" * 115)
        lines.append("Priority Legend: [!] High / Must Have | [-] Medium / Should Have | [*] Low / Could Have")
        return "\n".join(lines)
