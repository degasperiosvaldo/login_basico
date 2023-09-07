import streamlit as st
import pandas as pd
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def main():
	st.title("Entrada do Sistema ")
	menu = ["Início","Login","Increver"]
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Início":
		st.subheader("Início")
	elif choice == "Login":
		st.subheader("Seção de login")
		username = st.sidebar.text_input("Usuário")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))
				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				if task == "Add Post":
					st.subheader("Adicione sua postagem")
				elif task == "Analytics":
					st.subheader("Análise")
				elif task == "Profiles":
					st.subheader("Perfis de usuários")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Usuário ou senha incorretos")
	elif choice == "Increver":
		st.subheader("Cria nova conta")
		new_user = st.text_input("Usuário")
		new_password = st.text_input("Senha",type='password')
		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("Conta criada com sucesso.")
			st.info("Volte para o Login")
if __name__ == '__main__':
	main()
