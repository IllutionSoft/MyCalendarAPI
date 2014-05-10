from eve import Eve
import os
app = Eve()
import settings

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=9999)