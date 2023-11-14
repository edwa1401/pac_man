def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_block_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
            ])
    for block_num in range(1, vertical_wall_block_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
            ])
    return walls_coordinates


def calculate_block_coordinates(screen_width, screen_height, wall_block_width, wall_block_height, 
                                    horizontal_number=4, vertical_number=4):
    block_coordinates = []

    for block_horizontal_num in range(horizontal_number - 1, horizontal_number + 2):
        block_coordinates.extend([
            (block_horizontal_num * wall_block_width, wall_block_height * 4),
            (block_horizontal_num * wall_block_width, wall_block_height * 12),
            (screen_width - block_horizontal_num * wall_block_width - wall_block_width, wall_block_height * 4),
            (screen_width - block_horizontal_num * wall_block_width - wall_block_width * 7, wall_block_height * 8),
            (screen_width - block_horizontal_num * wall_block_width - wall_block_width, wall_block_height * 12),
            ])
        
    for block_vertical_num in range(vertical_number - 2, vertical_number + 2):
        block_coordinates.extend([

            (wall_block_width * 2, block_vertical_num * wall_block_height),
            (wall_block_width * 10, block_vertical_num * wall_block_height),
            (screen_width - wall_block_width * 2 - wall_block_width, block_vertical_num * wall_block_height),
            (wall_block_width * 2, screen_height - block_vertical_num * wall_block_height - wall_block_width ),
            (wall_block_width * 10, screen_height- block_vertical_num * wall_block_height - wall_block_width),
            (screen_width - wall_block_width * 2 - wall_block_width, screen_height - block_vertical_num * wall_block_height - wall_block_width)
            ])

    return block_coordinates
