from  app.models import create_databaseConnection








def customers_location_by_state():
    query = """
        SELECT 
        CASE 
            WHEN state_address IS NULL THEN 'Unknown'
            WHEN state_address NOT IN (
                'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 
                'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 
                'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 
                'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC') THEN 'Other'
            ELSE state_address
        END AS state_group, 
        COUNT(*) AS customer_count
        FROM customers
        GROUP BY state_group
        ORDER BY customer_count DESC;
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all the rows in a list of lists.
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


# data=customers_location_by_state()
# state_group=[]
# counts= []
# for states,count in data:
# 	state_group.append(states)
# 	counts.append(count)

# print(state_group)
# print(counts)
