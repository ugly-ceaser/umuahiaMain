# Deployment Guide for Render

## Steps to Deploy on Render

Follow these steps to successfully deploy your Django application on Render.

### 1. Update `build` Command

Modify the build command in Render to install dependencies and collect static files:

```sh
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

### 2. Configure Environment Variables

Set the following environment variables in Render:

#### **Basic Configurations**

| Variable     | Value                                       |
| ------------ | ------------------------------------------- |
| `SECRET_KEY` | QPpDGMDtSPfvffnRFqolqrscq7YC4rW8            |
| `DEBUG`      | false                                       |
| `APP_NAME`   | Umuahia Ireland                             |
| `APP_URL`    | _Replace this with the URL given by Render_ |

#### **Database Configuration**

Comment out the local database settings in `settings.py` and uncomment the hosted PostgreSQL database connection.

#### **Email Configuration**

| Variable              | Value                         |
| --------------------- | ----------------------------- |
| `EMAIL_HOST_USER`     | ifeanyionyekwelu786@gmail.com |
| `EMAIL_HOST_PASSWORD` | ucnn oizy lzld kzxd           |

### 3. Update Application URL After Deployment

Once Render provides the deployment URL, update the `APP_URL` variable to enable proper verification and functionality.

### 4. Migrate the Database

After deployment, run the following command on Render’s shell to apply database migrations:

```sh
python manage.py migrate
```

### 5. Verify the Deployment

- Open the deployed application in your browser.
- Check if static files load properly.
- Ensure database operations work correctly.
- Verify email functionalities.

### Notes

- Keep your environment variables secure.
- If you encounter issues, check Render’s logs for debugging.
- Ensure the `DEBUG` mode is set to `false` for production security.

Happy coding! 🚀
