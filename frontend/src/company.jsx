import React, { useState, useEffect } from "react";
import axios from "axios";

// Componente do Modal de Cadastro
const CadastroModal = ({ show, onClose, onAddEmpresa }) => {
    const [formData, setFormData] = useState({
        nome: '',
        cnpj: '',
        cidade: '',
        ramo: '',
        telefone: '',
        email: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post(
              "http://127.0.0.1:8000/empresas/",
              {
                nome: formData.nome,
                cnpj: formData.cnpj,
                cidade: formData.cidade,
                ramo_atuacao: formData.ramo,
                telefone: formData.telefone,
                email_contato: formData.email
              },
              { headers: { "Content-Type": "application/json" } }
            );
            
            setFormData({ nome: '', cnpj: '', cidade: '', ramo: '', telefone: '', email: ''});

            alert("Empresa cadastrada com sucesso!");   
            
             onAddEmpresa();

        } catch (error) {
            if (error.response && error.response.status === 400) {
                alert("CNPJ ou Email já cadastrado");
            } else {
                alert("Erro ao tentar cadastrar a empresa.");
            }
        }
        onClose();
    };

    if (!show) {
        return null;
    }

    return (
        <div className="modal" style={{ display: 'flex' }}>
            <div className="modal-content">
                <span className="close-btn" onClick={onClose}>&times;</span>
                <h2>Cadastro de Empresas</h2>
                <form id="cadastro-form" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="nome-modal">Nome da Empresa</label>
                        <input type="text" id="nome-modal" name="nome" value={formData.nome} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="cnpj-modal">CNPJ</label>
                        <input type="text" id="cnpj-modal" name="cnpj" value={formData.cnpj} onChange={handleChange} placeholder="00.000.000/0000-00" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="cidade-modal">Cidade</label>
                        <input type="text" id="cidade-modal" name="cidade" value={formData.cidade} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="ramo-modal">Ramo de Atuação</label>
                        <input type="text" id="ramo-modal" name="ramo" value={formData.ramo} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="telefone-modal">Telefone</label>
                        <input type="text" id="telefone-modal" name="telefone" value={formData.telefone} onChange={handleChange} placeholder="(99) 99999-9999" required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email-modal">E-mail</label>
                        <input type="email" id="email-modal" name="email" value={formData.email} onChange={handleChange} required />
                    </div>
                    <button type="submit">Cadastrar</button>
                </form>
            </div>
        </div>
    );
};

// Componente Principal do App
const App = () => {
    const [empresas, setEmpresas] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchEmpresas = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get("http://127.0.0.1:8000/empresas");
            setEmpresas(response.data);
        } catch (err) {
            setError('Falha ao carregar a lista de empresas.');
            console.error("Fetch error: ", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEmpresas();
    }, []);

    const handleRemoveEmpresa = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/empresas/${id}`);
            fetchEmpresas();
        } catch (err) {
            setError('Falha ao remover a empresa.');
            console.error(err);
        }
    };

    const filteredEmpresas = empresas.filter(empresa =>
        empresa.nome.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <React.Fragment>
            <div className="container1">
                <h2>Gerenciamento de Empresas</h2>
                <div className="header">
                    <div className="input-group">
                        <input
                            type="text"
                            id="search-input"
                            placeholder="Pesquisar por nome da empresa..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <button onClick={() => setIsModalOpen(true)}>Nova Empresa</button>
                </div>
                {loading && <p>Carregando empresas...</p>}
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {!loading && !error && (
                    <ul id="lista-empresas" className="task-list">
                        {filteredEmpresas.length > 0 ? (
                            filteredEmpresas.map((empresa, index) => (
                                <li key={empresa.id || index} className="task-item">
                                    <span className="task-text">{empresa.nome} - CNPJ: {empresa.cnpj}</span>
                                    <button className="task-remove-btn" onClick={() => handleRemoveEmpresa(empresa.id)}>&times;</button>
                                </li>
                            ))
                        ) : (
                            <p>Nenhuma empresa encontrada.</p>
                        )}
                    </ul>
                )}
                <CadastroModal 
                    show={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    onAddEmpresa={fetchEmpresas}
                />
            </div>
        </React.Fragment>
    );
};

export default App;
