import React, { useState } from "react";
import axios from "axios";
import './index.css';

const App = () => {
  const [form, setForm] = useState({ nome: "", senha: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/admin", 
        new URLSearchParams({
          username: form.nome,
          password: form.senha
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      // Extrai o token da resposta do servidor
      const token = response.data.access_token;
      
      // Armazena o token no LocalStorage 
      localStorage.setItem('access_token', token);

      // limpar os campos
      setForm({ nome: "", senha: "" });

      alert("Logado com sucesso!");      
      window.location.href = "company_registration.html";

    } catch (error) {
      if (error.response && error.response.status === 401) {
        alert("Credenciais Inválidas.");
      } else {
        alert("Erro ao tentar fazer login.");
      }
    }
  };

  return (
    <div className="container">
      <h2>Entrar como Administrador</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nome:</label>
          <input 
            type="text" 
            id="nome" 
            name="nome" 
            value={form.nome} 
            onChange={handleChange} 
            placeholder="Digite um nome: "
          />
        </div>
        <div className="form-group">
          <label>Senha:</label>
          <input 
            type="password" 
            id="senha" 
            name="senha" 
            value={form.senha} 
            onChange={handleChange} 
            placeholder="Digite uma senha: "
          />
        </div>
        <button type="submit">Entrar</button>       
      </form>
    </div>
  );
};

export default App;