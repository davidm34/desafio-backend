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
        <h2>Cadastro de Empresas</h2>
        <form>
            <div class="form-group">
                <label for="nome">Nome da Empresa</label>
                <input type="text" id="nome" name="nome" required />
            </div>
            <div class="form-group">
                <label for="cnpj">CNPJ</label>
                <input type="text" id="cnpj" name="cnpj" placeholder="00.000.000/0000-00" required />
            </div>
            <div class="form-group">
                <label for="cidade">Cidade</label>
                <input type="text" id="cidade" name="cidade" required/>
            </div>
            <div class="form-group">
                <label for="ramo">Ramo de Atuação</label>
                <input type="text" id="ramo" name="ramo" required/>
            </div>
            <div class="form-group">
                <label for="telefone">Telefone</label>
                <input type="text" id="telefone" name="telefone" placeholder="(99) 99999-9999" required/>
            </div>
            <div class="form-group">
                <label for="email">E-mail</label>
                <input type="email" id="email" name="email" required/>
            </div>
            <button type="submit">Cadastrar</button>
        </form>
    </div>

  );
};

export default App;