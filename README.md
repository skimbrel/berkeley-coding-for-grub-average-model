# Example: Average-rating model for Berkeley Coding for Grub challenge

This produces a slightly more intelligent model: it uses the training data to record
the average stars for each business it sees and each user it sees. To form a hypothesis about
a new review, it takes the average of the average rating for the business and user in the review.

## Usage

python average_model.py training_data.json testing_data.json > hypothesis.json
curl -Fhypothesis=@hypothesis.json http://yelp-csua-coding.herokuapp.com/rmse

## Resources

http://www.yelp.com/academic_dataset

test_reviews.json available to Berkeley students during the competition

To test results http://yelp-csua-coding.herokuapp.com/rmse

## License

Copyright 2009-2012 Yelp (Sam Kimbrel skimbrel@yelp.com)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
