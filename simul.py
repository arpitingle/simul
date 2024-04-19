import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100

    def move(self):
        # Determine the direction of movement
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)

        # Check if the new position is within the boundaries
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x <= 10 and 0 <= new_y <= 10:
            self.x = new_x
            self.y = new_y
        else:
            # Bounce back if the new position is outside the boundaries
            self.x -= dx
            self.y -= dy

        self.energy -= 1

    def eat(self):
        self.energy += 20

class Predator(Creature):
    def __init__(self, x, y):
        super().__init__(x, y)

    def hunt(self, prey):
        if abs(self.x - prey.x) <= 1 and abs(self.y - prey.y) <= 1:
            prey.energy -= 30
            self.energy += 50

class Prey(Creature):
    def __init__(self, x, y):
        super().__init__(x, y)

    def reproduce(self):
        if self.energy >= 200:
            self.energy /= 2
            return Prey(self.x, self.y)

# Create initial population
predators = [Predator(random.randint(0, 10), random.randint(0, 10)) for _ in range(5)]
preys = [Prey(random.randint(0, 10), random.randint(0, 10)) for _ in range(20)]

# Create a figure and axis for the animation
fig, ax = plt.subplots(figsize=(8, 8))

# Create scatter plot for predators and preys
predator_plot = ax.scatter([predator.x for predator in predators], [predator.y for predator in predators], color='red', label='Predators')
prey_plot = ax.scatter([prey.x for prey in preys], [prey.y for prey in preys], color='blue', label='Preys')
ax.set_title('Predator-Prey Simulation')
ax.legend()

# Remove axis ticks and numbers
ax.set_xticks([])
ax.set_yticks([])

# Create a text box to display the number of predators and preys
text_box = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

# Update function for animation
def update(frame):
    global predators, preys

    # Move creatures
    for creature in predators + preys:
        creature.move()

    # Predators hunt
    for predator in predators:
        for prey in preys:
            predator.hunt(prey)

    # Preys reproduce
    new_preys = []
    for prey in preys:
        new_prey = prey.reproduce()
        if new_prey:
            new_preys.append(new_prey)
    preys.extend(new_preys)

    # Remove dead preys
    preys = [prey for prey in preys if prey.energy > 0]

    # Update scatter plot data
    predator_plot.set_offsets([(predator.x, predator.y) for predator in predators])
    prey_plot.set_offsets([(prey.x, prey.y) for prey in preys])

    # Update text box with the number of predators and preys
    text_box.set_text(f'Predators: {len(predators)}\nPreys: {len(preys)}')

    # Stop the animation if all preys have died
    if len(preys) == 0:
        ani.event_source.stop()

    return predator_plot, prey_plot, text_box

# Create animation
ani = FuncAnimation(fig, update, frames=None, blit=True, repeat=True)
plt.show() 