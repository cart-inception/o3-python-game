class Theme:
    def __init__(self, name, description, benefits):
        self.name = name
        self.description = description
        self.benefits = benefits

    def display_info(self):
        return f"Theme: {self.name}\nDescription: {self.description}\nBenefits: {', '.join(self.benefits)}"


class OffGridLivingTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Off-Grid Living",
            description="A sustainable lifestyle that minimizes reliance on public utilities.",
            benefits=[
                "Reduced carbon footprint",
                "Self-sufficiency",
                "Connection with nature",
                "Lower living costs"
            ]
        )


class TechSustainabilityTheme(Theme):
    def __init__(self):
        super().__init__(
            name="Tech Sustainability",
            description="Integrating technology with sustainable practices for efficient living.",
            benefits=[
                "Smart resource management",
                "Enhanced productivity",
                "Innovative farming techniques",
                "Waste reduction"
            ]
        )


def get_themes():
    return [OffGridLivingTheme(), TechSustainabilityTheme()]