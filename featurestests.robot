* Settings *
Library  OperatingSystem
Library  RequestsLibrary
Library  Collections

* Variables *
${BASE_URL}      http://localhost:8080   # Assuming the API runs locally on port 8080
${RESERVATION_ID}    # Variable to store the reservation ID for canceling

* Test Cases *
Make a Reservation
    [Documentation]    Test making a new reservation
    Create Session    Dog Spa API    ${BASE_URL}
    ${response}=    Post Request    Dog Spa API    /make_reservation    json={"start_time": "2023-11-06T09:00:00"}
    Should Be Equal As Strings    ${response.status_code}    200
    ${json_response}=    Set Variable    ${response.json()}
    Should Be True    ${json_response["success"]}
    Log    Reservation made successfully.

Cancel Reservation
    [Documentation]    Test canceling an existing reservation
    Create Session    Dog Spa API    ${BASE_URL}
    ${response}=    Post Request    Dog Spa API    /cancel_reservation    json={"start_time": "2023-11-06T09:00:00"}
    Should Be Equal As Strings    ${response.status_code}    200
    ${json_response}=    Set Variable    ${response.json()}
    Should Be True    ${json_response["success"]}
    Log    Reservation canceled successfully.

View Reservations
    [Documentation]    Test viewing existing reservations
    Create Session    Dog Spa API    ${BASE_URL}
    ${response}=    Get Request    Dog Spa API    /view_reservations
    Should Be Equal As Strings    ${response.status_code}    200
    ${reservations}=    Set Variable    ${response.json()["reservations"]}
    Should Not Be Empty    ${reservations}
    Log Many    ${reservations}

* Keywords *
Log Many
    [Arguments]    ${list}
    :FOR    ${item}    IN    @{list}
    \    Log    ${item}