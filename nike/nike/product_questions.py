# myproject/myproject/questions.py
class ProductQuestions:
    @staticmethod
    def ask_sex():
        return input("Enter the sex (man, woman): ")

    @staticmethod
    def ask_product_type():
        return input("Enter the product type (clothes, shoes): ")

    @staticmethod
    def ask_size():
        sizes = input("Enter the sizes (comma-separated, e.g., xs,s,m,l,xl): ")
        return [size.strip() for size in sizes.split(',')]

    @staticmethod
    def ask_color():
        colors = input("Enter the colors (comma-separated): ")
        return [color.strip() for color in colors.split(',')]

    @staticmethod
    def ask_max_price():
        return int(input("Enter the max price: "))
    @staticmethod
    def ask_min_price():
        return int(input("Enter the min price: "))