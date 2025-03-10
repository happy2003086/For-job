from datetime import datetime, timedelta, timezone

def get_world_time(city, offset_hours):
  """
  Gets the current time for a given city and its UTC offset.

  Args:
    city: The name of the city.
    offset_hours: The UTC offset in hours.

  Returns:
    A string representing the current time in the given city.
  """

  utc_time = datetime.now(timezone.utc)
  city_time = utc_time + timedelta(hours=offset_hours)
  return f"Current time in {city}: {city_time.strftime('%Y-%m-%d %H:%M:%S')}"

# Example usage:
cities_and_offsets = {
    "New York": -5,
    "London": 0,
    "Tokyo": 9,
    "Sydney": 11,
    "Rio de Janeiro": -3
}

for city, offset in cities_and_offsets.items():
  print(get_world_time(city, offset))
1
1
123