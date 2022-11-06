# Theia

![Theia Logo](theia.png "Theia")

## Inspiration

We both have aspirations to travel the world and we thought it would be handy to have an all-in-one travel app in our back pocket. So we created Theia. Theia is the Greek Goddess of vision. We chose this name because our app allows the user to see and understand many foreign ideas.

## What it does

Our application is a resource for tourists. Theia allows users to scan foreign prices and have them automatically converted into USD. Not only does Theia convert currency, but it can have users scan foreign text and translate it into English and also give the users the ability to record and translate foreign speech.

## How we built it

We built this application using Google Cloud. This is a pure python codebase with a Qt GUI. We were able to implement Google Cloud Vision, Google Cloud Translation, and Google Cloud Speech-to-Text AI technology. It was a privilege to work with such reliable software. We also used openCV to have a video feed that fed into the Google Cloud AI APIs. We also used the ExchangeRate-API to reliably pull up-to-date exchange rates.

## Challenges we ran into

When we tried to integrate the audio input component, we encountered issues where the app would freeze up.

## Accomplishments that we're proud of

We’re very proud that we were able to use AI technology to have such a strong potential impact on tourists that are traveling to a new country. This was all thanks to the great AI behind the scenes with three unique machine-learning Google Cloud APIs.

## What we learned

We learned a lot about cloud computing as well as machine learning. We also became significantly more comfortable working as a team to produce a larger python project.

## What's next for Theia

We would like to continue the implementation of our live speech translator with the hopes of better connecting people and breaking the language barrier. Soon to come is a scrollable map, ride-sharing capabilities, lodging data, and live flight data. Theia is your all-in-one travel partner!

## Running Theia

```bash
$ python3 main.py
```
