🩸Blood SOS – Emergency Blood Request System

A full-stack web application that allows hospitals to raise emergency blood requests and connect with registered donors efficiently.

This project demonstrates backend development, authentication, database integration, and frontend–backend communication using Flask.

Features

**Hospital**
	•	Register hospital details
	•	Login using OTP authentication
	•	Raise emergency SOS request
** Donor **
	•	Register as donor
	•	Store blood group and contact details
	•	Store current location (Latitude & Longitude)

** Twilio SMS API **

The application integrates Twilio SMS API to notify registered donors when a hospital raises an emergency blood request (SOS).

When an SOS is triggered:
	•	The backend filters donors by blood group
	•	SMS notifications are sent automatically
	•	Donors receive hospital contact details instantly

** Tech Stack **

Frontend:
	•	HTML
	•	CSS
	•	JavaScript

Backend:
	•	Python
	•	Flask

Database:
	•	MongoDB

