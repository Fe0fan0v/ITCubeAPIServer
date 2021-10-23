import uvicorn

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, workers=4, host='127.0.0.1', port=8000)