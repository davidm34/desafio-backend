import React, { useState, useEffect } from "react";
import axios from "axios";
import './index.css';

const App = () => {
  const [form, setForm] = useState({ nome: "", senha: ""});

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {

      await axios.post("http://127.0.0.1:8000/admin/", form);
      setForm({ nome: "", senha: "" });
      alert("Logado com sucesso!");      
    } catch (error) {
      if (error.response && error.response.status === 401) {
        alert("Credenciais Inválidas.");
      } else {
        alert("Erro ao verificar ou criar o adminstrador.");
      }
    }
  };


  return (
    <div class="container">
        <h2>Entrar como Adminstrador</h2>
        <form onSubmit={handleSubmit}>
            <div class="form-group">
                <label>Nome:</label>
                <input type="text" id="nome" name="nome" value={form.nome} onChange={handleChange} placeholder="Digite um nome: "/>
            </div>
            <div class="form-group">
                <label>Senha:</label>
                <input type="text" id="senha" name="senha" value={form.senha} onChange={handleChange} placeholder="Digite uma senha: "/>
            </div>
            <button type="submit">Entrar</button>       
        </form>
    </div>

  );
};

export default App;