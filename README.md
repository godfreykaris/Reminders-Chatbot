# Reminders

Reminders is a goal monitoring application that helps users track their goals and receive reminder messages through WhatsApp. It also provides AI-generated reports based on user responses stored in the database.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Adding Goals](#adding-goals)
  - [Receiving Reminder Messages](#receiving-reminder-messages)
  - [Viewing AI-Generated Reports](#viewing-ai-generated-reports)
  - [Managing User Profile](#managing-user-profile)
    - [Editing Profile](#editing-profile)
    - [Changing Password](#changing-password)
    - [Logging Out](#logging-out)
- [Supabase Database](#supabase-database)
- [WhatsApp Integration](#whatsapp-integration)
- [Testing Locally](#testing-locally)
- [User Interface Customization](#user-interface-customization)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

Follow the instructions below to set up and use the Reminders application.

### Prerequisites

Before installing the Reminders application, ensure that you have the following packages installed globally on your system:

- `psycopg2-binary`
- `openai`
- `twilio`
- `python-Levenshtein`

These packages are needed to run the system's cron jobs.

### Installation

1. Clone the Reminders repository from GitHub:

   ```shell
   git clone https://github.com/godfreykaris/Reminders-Chatbot.git
# Project Name

2. **Change into the project directory and install the necessary dependencies:**

    ```shell
    pip install -r requirements.txt
    ```

3. **Update the configuration file:**

    - Open `config.json` in the project's root directory and add your specific details:

    ```json
    {
      "db_host": "your-db-host",
      "db_port": "your-db-port",
      "db_name": "your-db-name",
      "db_user": "your-db-user",
      "db_password": "your-db-password",
      "twilio_sid": "your-twilio-sid",
      "twilio_token": "your-twilio-token",
      "from_phone_number_sms": "your-sms-phone-number",
      "from_phone_number_whatsapp": "your-whatsapp-phone-number",
      "openai_key": "your-openai-key"
    }
    ```

    Replace the placeholders with your actual values.

4. **Create a `.env` file:**

    - In the project's root directory, create a `.env` file and add the following variables:

    ```dotenv
    MAIL_USERNAME=your-email-username
    MAIL_PASSWORD=your-email-password
    MAIL_DEFAULT_SENDER=your-email-default-sender
    SECRET_KEY=your-secret-key
    ```

    These variables are used for password reset emails.

5. **Start the application:**

    ```shell
    python3 main.py
    ```

    The Reminders application should now be running on your local machine.

## Configuration

The Reminders application requires configuration files to set up database connections, Twilio integration, OpenAI API integration, and email settings. Ensure that you have updated the `config.json` file and created the `.env` file as mentioned in the installation steps.

## Usage

### Adding Goals

To add a goal, follow these steps:

1. Open the Reminders application in your web browser.
2. Log in using your credentials or create a new account if you don't have one.
3. Navigate to the "Goals" section.
4. Click on the "Add Goal" button.
5. Enter the details of your goal, such as the title, description, due date, time of day, time zone, and contact preference.
6. Click "Add Goal" to add the goal.

### Receiving Reminder Messages

The Reminders application sends reminder messages through WhatsApp to help you stay on track with your goals. In a real-world deployment, the owner of the app should use purchased phone numbers from Twilio, and WhatsApp sandboxes are only used for testing purposes.

The Reminders application uses the WhatsApp sandbox to send and receive messages via WhatsApp. To join the WhatsApp sandbox, send the message join pet-meat to the WhatsApp sandbox number: +14155238886.

It also uses sms service but may incur charges.

Make sure you configure webhooks for both sms and whatsapp correctly like:

THE_APP'S_BASE_URL/api/webhook/whatsapp
THE_APP'S_BASE_URL/api/webhook/sms


### Viewing AI-Generated Reports

The Reminders application generates AI-based reports to provide insights into your goal progress.

1. Navigate to the "Reports" section in the application.
2. The reports will be displayed, showcasing your progress and suggesting improvements based on your responses.

### Managing User Profile

#### Editing Profile

To edit your profile, follow these steps:

1. Log in to the Reminders application.
2. Navigate to the "Profile" section.
3. Click on the "Edit Profile" button.
4. Update the desired fields, such as name, email, and phone number.
5. Click "Update Profile" to update your profile.

#### Changing Password

To change your password, follow these steps:

1. Log in to the Reminders application.
2. Navigate to the "Profile" section.
3. Click on the "Change Password" button.
4. Enter your current password and the new password.
5. Click "Change Password" to change your password.

#### Logging Out

To log out of the Reminders application, click on the "Logout" button in the Profile secion.

## Supabase Database

The Reminders application uses a Supabase database to store user data, goals, and progress. For more information on how to set up and configure Supabase, refer to the Supabase Documentation.

The Reminders application uses Supabase as the database, consisting of the following tables:

### `users`

**Columns:**

- `id` (Primary Key)
- `created_at`
- `email`
- `phone_number`
- `password_hash`
- `updated_at`
- `name`

### `goals`

**Columns:**

- `id` (Primary Key)
- `created_at`
- `user_id` (Foreign Key)
- `goal_title`
- `goal_description`
- `time_of_day`
- `time_zone`
- `contact_choice`
- `report_frequency`

### `goal_data`

**Columns:**

- `id` (Primary Key)
- `created_at`
- `user_id` (Foreign Key)
- `goal_id` (Foreign Key)
- `feedback`

The `user_id` and `goal_id` columns in the `goal_data` table are foreign keys, and deletion of records is cascaded.


## WhatsApp Integration

The Reminders application integrates with WhatsApp to send reminder messages. For more information on how to set up WhatsApp integration, refer to the Twilio API for WhatsApp Documentation.

## Testing Locally

To test the Reminders application locally, follow these steps:

1. Set up a local PostgreSQL database.
2. Update the `config.json` file with your local database details.
3. Create a virtual environment (recommended).
4. Install the necessary dependencies using `pip install -r requirements.txt`.
5. Start the application using `python3 main.py`.

## User Interface Customization

The Reminders application's user interface can be customized by modifying the HTML, CSS, and JavaScript files located in the templates and static directories.

## Contributing

Contributions to the Reminders application are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes.
4. Test your changes.
5. Commit and push your changes to your forked repository.
6. Submit a pull request.

## License

The Reminders application is licensed under the MIT License.

## Acknowledgments

Special thanks to the following libraries and frameworks used in this project:

- Flask
- Supabase
- Twilio
- OpenAI
- Svelte
- Flowbite
- Tailwind CSS
