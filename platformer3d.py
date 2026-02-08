from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Sky + light
Sky()
DirectionalLight()

# Player
player = FirstPersonController(
    position=(0, 2, 0),
    speed=7,
    jump_height=3
)

# Ground (single plane, no glitches)
ground = Entity(
    model='plane',
    scale=50,
    texture='white_cube',
    texture_scale=(50, 50),
    collider='box',
    color=color.rgb(300, 120, 80)
)

block_texture = 'white_cube'
placed_blocks = {}   # dictionary to prevent duplicates


class Block(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=block_texture,
            color=color.color(5, 0, random.uniform(0.9, 1)),
            highlight_color=color.lime,
            collider='box'
        )

    def input(self, key):
        # Remove block
        if self.hovered and key == 'left mouse down':
            pos_key = tuple(self.position)
            if pos_key in placed_blocks:
                del placed_blocks[pos_key]
            destroy(self)

        # Place block on top
        if self.hovered and key == 'right mouse down':
            new_pos = self.position + mouse.normal
            pos_key = tuple(new_pos)

            if pos_key not in placed_blocks:
                placed_blocks[pos_key] = Block(position=new_pos)


def input(key):
    # Allow placing blocks directly on the ground
    if key == 'right mouse down' and mouse.hovered_entity == ground:
        hit_pos = mouse.world_point
        grid_pos = round(hit_pos.x), 1, round(hit_pos.z)

        if grid_pos not in placed_blocks:
            placed_blocks[grid_pos] = Block(position=grid_pos)

    # Remove blocks on ground level (optional)
    if key == 'left mouse down' and mouse.hovered_entity == ground:
        pass  # do nothing
    


def update():
    pass


app.run()

