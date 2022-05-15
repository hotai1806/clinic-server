curl --request POST \
--url https://api.sendgrid.com/v3/mail/send \
--header 'Authorization: Bearer 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' \
--header 'Content-Type: application/json' \
--data '{"personalizations":[{"to":[{"email":"taiht.jul@gmail.com"}],"subject":"Hello, World!"}],"content": [{"type": "text/plain", "value": "Heya!"}],"from":{"email":"sam.smith@example.com","name":"Sam Smith"},"reply_to":{"email":"sam.smith@example.com","name":"Sam Smith"}}'
