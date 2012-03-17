from __future__ import print_function

from math import ceil
from math import floor
from sys import argv
from sys import stderr

import simplejson

def generate_model(training_data):
    """Given an iterable of lines of JSON containing user and business data,
    build and return a predictive model for future reviews.

    Args:
        - training_data: An iterable of JSON data
    """

    user_averages = {}
    business_averages = {}

    for line in training_data:
        # Each line of the input data is a JSON dictionary object containing a record.
        # Use simplejson's loads() function to parse this into a native Python dictionary.
        parsed_data = simplejson.loads(line)

        if parsed_data.get('review_id', None) is not None:
            # Skip review records for this example since we don't need them.
            continue

        user_id = parsed_data.get('user_id', None)
        business_id = parsed_data.get('business_id', None)

        if user_id is not None:
            user_averages[user_id] = parsed_data['average_stars']
        elif business_id is not None:
            business_averages[business_id] = parsed_data['stars']
        else:
            print("Record has neither a business_id nor a user_id: %s" % line, file=stderr)

    return user_averages, business_averages

def predict_reviews(review_data, user_averages, business_averages):
    """Given an iterable of lines of JSON containing reviews and a trained model,
    output predicted star ratings for each review.

    Args:
        - review_data: An iterable of JSON review data
        - user_averages: A dict mapping user_id => average stars
        - business_averages: A dict mapping business_id => average stars
    """

    for raw_review in review_data:
        # Each line of the testing data is a JSON dictionary object containing a review record.
        # Use simplejson's loads() function to parse this into a native Python dictionary.
        review = simplejson.loads(raw_review)

        review_id = review.get('review_id', None)
        if review_id is None:
            print("Review record has no ID! %s" % raw_review, file=stderr)
            continue

        business_id = review.get('business_id', None)
        user_id = review.get('user_id', None)

        if business_id is None or user_id is None:
            print("Review record is incomplete: %s" % raw_review, file=stderr)
            continue

        user_average = user_averages.get(user_id, None)
        business_average = business_averages.get(business_id, None)

        guess = 3 # Set an initial guess in case we have no data.
        if user_average is not None and business_average is not None:
            guess = (user_average + business_average) / 2.0
        elif user_average is not None:
            guess = user_average
        else:
            guess = business_average

        # Do slightly more accurate rounding rather than just truncating.
        if guess > floor(guess) + 0.5:
            guess = ceil(guess)
        else:
            guess = floor(guess)

        output = {
            'review_id': review_id,
            'stars': guess,
        }

        # Use simplejson's dumps() function to encode our output dict as a JSON
        # dictionary, and print the result to stdout.
        print(simplejson.dumps(output))

def train_and_predict(training_filename, test_filename):
    with open(training_filename) as training_file:
        user_averages, business_averages = generate_model(training_file)

    with open(test_filename) as test_file:
        predict_reviews(test_file, user_averages, business_averages)

if __name__ == '__main__':
    if len(argv) != 3:
        print("usage: %s training-data.json test-data.json" % argv[0])
    training_filename = argv[1]
    test_filename = argv[2]

    train_and_predict(training_filename, test_filename)
