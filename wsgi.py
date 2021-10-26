'''Точка входа в приложение. Запускаем uvicorn-worker, расчет по количеству процессов - на одно ядро два процесса + 1'''
import uvicorn
from main import app

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, host='127.0.0.1', port=8000)
