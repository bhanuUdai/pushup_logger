from pushups_logger import create_app 
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode if executed directly
    app.run()