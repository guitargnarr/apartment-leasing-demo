"""
WebSocket Manager
Real-time connection management for instant unit updates
"""

from fastapi import WebSocket
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time updates
    Broadcasts unit changes to all connected clients instantly
    """

    def __init__(self):
        # List of active WebSocket connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accept new WebSocket connection and add to active connections
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """
        Remove WebSocket connection from active connections
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send message to specific WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: dict):
        """
        Broadcast message to all connected clients
        This is the key method for real-time updates

        Args:
            message: Dictionary containing message type and data
        """
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_unit_update(self, unit_data: dict):
        """
        Broadcast unit update to all connected clients
        Specialized method for unit changes

        Args:
            unit_data: Dictionary containing updated unit information
        """
        message = {
            "type": "unit_update",
            "data": unit_data
        }
        await self.broadcast(message)

    async def broadcast_unit_deleted(self, unit_id: str):
        """
        Broadcast unit deletion to all connected clients

        Args:
            unit_id: ID of deleted unit
        """
        message = {
            "type": "unit_deleted",
            "data": {"id": unit_id}
        }
        await self.broadcast(message)

    async def broadcast_analytics_update(self, analytics_data: dict):
        """
        Broadcast analytics update to all connected clients

        Args:
            analytics_data: Dictionary containing analytics metrics
        """
        message = {
            "type": "analytics_update",
            "data": analytics_data
        }
        await self.broadcast(message)

    def get_connection_count(self) -> int:
        """
        Get number of active WebSocket connections

        Returns:
            Count of active connections
        """
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()
