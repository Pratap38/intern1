import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

# Shared in-memory state (good for assignment demo)
CLAIMED_BLOCKS = {}

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "block_game"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        self.color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        await self.send(json.dumps({
            "type": "user_color",
            "color": self.color
        }))

        # Send existing blocks to new user
        for (x, y), color in CLAIMED_BLOCKS.items():
            await self.send(json.dumps({
                "type": "block_claimed",
                "x": x,
                "y": y,
                "color": color
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "claim_block":
            x, y = data["x"], data["y"]
            key = (x, y)

            # Prevent double-claim
            if key in CLAIMED_BLOCKS:
                return

            CLAIMED_BLOCKS[key] = self.color

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "broadcast_claim",
                    "x": x,
                    "y": y,
                    "color": self.color
                }
            )

    async def broadcast_claim(self, event):
        await self.send(json.dumps({
            "type": "block_claimed",
            "x": event["x"],
            "y": event["y"],
            "color": event["color"]
        }))
