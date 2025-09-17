from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_task_update(task):
    created = task.created
    assigned = task.assigned
    channel_layer = get_channel_layer()

    payload = {
        "type": "task_update",
        "data": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "assigned": assigned.email if assigned else None,
            "created": created.email if created else None,
        },
    }

    print("Preparing to notify via WebSocket")
    for user in [created, assigned]:
        if user:
            group_name = f"user_{user.id}"
            print(f"[Websocket Notify] Sending update to group: {group_name}")
            async_to_sync(channel_layer.group_send)(group_name, payload)