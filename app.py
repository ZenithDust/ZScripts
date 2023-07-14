from src import create_app, break_after_first

app = create_app()

if __name__ == "__main__":
  app.jinja_env.filters['break_after_first'] = break_after_first
  app.run(host="0.0.0.0", debug=False)