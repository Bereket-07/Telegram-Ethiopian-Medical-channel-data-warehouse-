SELECT
    "ID",
    "Channel Title",
    "Channel Username",
    "Message",
    "Date",
    "Media Path"
FROM
    medical_data
WHERE
    "Message" IS NOT NULL 
