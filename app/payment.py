from database import mark_fine_paid

def process_payment(plate):
    mark_fine_paid(plate)
