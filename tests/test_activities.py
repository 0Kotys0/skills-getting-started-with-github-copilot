def test_root_redirect(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert "participants" in data[expected_activity]
    assert "description" in data[expected_activity]


def test_signup_success(client):
    # Arrange
    activity_name = "Soccer Club"
    student_email = "alex@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"

    activities_response = client.get("/activities")
    assert student_email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate_error(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    student_email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    registered_email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": registered_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {registered_email} from {activity_name}"

    activities_response = client.get("/activities")
    assert registered_email not in activities_response.json()[activity_name]["participants"]


def test_unregister_not_registered_error(client):
    # Arrange
    activity_name = "Chess Club"
    unregistered_email = "nobody@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": unregistered_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_nonexistent_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
