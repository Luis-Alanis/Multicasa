// ========== CONFIGURACIÓN Y CONSTANTES ==========

const CONFIG = {
    entities: {
        casa: {
            apiUrl: '/api/casas',
            idField: 'id_casa',
            titleNew: 'Nueva Casa',
            titleEdit: 'Editar Casa',
            template: 'template-casa-row',
            fields: ['id_locacion', 'latitud', 'longitud', 'codigo_postal', 'costo', 'recamaras', 'baños', 'estatus_venta', 'fotos']
        },
        locacion: {
            apiUrl: '/api/locaciones',
            idField: 'id_locacion',
            titleNew: 'Nueva Locación',
            titleEdit: 'Editar Locación',
            template: 'template-locacion-row',
            fields: ['nombre']
        },
        usuario: {
            apiUrl: '/api/usuarios',
            idField: 'id_usuario',
            titleNew: 'Nuevo Usuario',
            titleEdit: 'Editar Usuario',
            template: 'template-usuario-row',
            fields: ['nombre', 'correo', 'telefono']
        }
    }
};

// ========== UTILIDADES DOM ==========

const DOM = {
    query: (selector, context = document) => context.querySelector(selector),
    queryAll: (selector, context = document) => context.querySelectorAll(selector),
    getByData: (attr, value, context = document) => context.querySelector(`[data-${attr}="${value}"]`),
    getAllByData: (attr, value, context = document) => context.querySelectorAll(`[data-${attr}="${value}"]`),
    cloneTemplate: (templateId) => {
        const template = document.getElementById(templateId);
        if (!template) {
            console.error(`Template ${templateId} no encontrado`);
            return null;
        }
        return template.content.cloneNode(true);
    }
};

// ========== GESTIÓN DE ESTADO ==========

const State = {
    currentTab: 'casa',
    currentEntity: null,
    currentId: null
};

// ========== RENDERIZADO ==========

const Renderer = {
    createRowFromTemplate(entity, item) {
        const config = CONFIG.entities[entity];
        const fragment = DOM.cloneTemplate(config.template);
        
        if (!fragment) {
            console.error(`No se pudo clonar el template para ${entity}`);
            return null;
        }
        
        // IMPORTANTE: Obtener el elemento TR del fragmento primero
        const row = fragment.querySelector('tr');
        if (!row) {
            console.error(`No se encontró TR en el template de ${entity}`);
            return null;
        }
        
        // Rellenar campos básicos
        const fields = row.querySelectorAll('[data-field]');
        fields.forEach(field => {
            const fieldName = field.dataset.field;
            
            if (fieldName === 'costo') {
                field.textContent = `$${Number(item.costo).toLocaleString('es-MX', {minimumFractionDigits: 2})}`;
            } else if (fieldName === 'codigo_postal') {
                field.textContent = item.codigo_postal || 'N/A';
            } else if (fieldName === 'telefono') {
                field.textContent = item.telefono || 'N/A';
            } else if (fieldName === 'estatus') {
                const statusSpan = document.createElement('span');
                statusSpan.className = 'status-badge';
                statusSpan.textContent = item.estatus_venta;
                if (item.estatus_venta === 'En Venta') {
                    statusSpan.classList.add('status-venta');
                } else {
                    statusSpan.classList.add('status-vendida');
                }
                field.innerHTML = '';
                field.appendChild(statusSpan);
            } else if (fieldName === 'value') {
                field.value = item[config.idField];
                field.textContent = item.nombre;
            } else {
                field.textContent = item[fieldName] || item[config.idField];
            }
        });
        
        // Configurar botones de acción con el ID correcto
        const buttons = row.querySelectorAll('[data-action]');
        buttons.forEach(button => {
            button.dataset.id = item[config.idField];
            button.dataset.entity = entity;
        });
        
        // Retornar el TR, no el fragmento
        return row;
    },
    
    renderList(entity, items) {
        const target = DOM.getByData('target', `${entity}-list`);
        if (!target) {
            console.error(`No se encontró el target para ${entity}-list`);
            return;
        }
        
        target.innerHTML = '';
        
        if (!items || items.length === 0) {
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = '<td colspan="100%" style="text-align: center; padding: 20px; color: #999;">No hay registros</td>';
            target.appendChild(emptyRow);
            return;
        }
        
        items.forEach(item => {
            const row = this.createRowFromTemplate(entity, item);
            if (row) {
                target.appendChild(row);
            }
        });
        
        console.log(`Renderizados ${items.length} items de ${entity}`);
    },
    
    renderLocacionSelect(locaciones) {
        const select = DOM.getByData('target', 'casa-locacion-select');
        if (!select) {
            console.error('No se encontró el select de locaciones');
            return;
        }
        
        select.innerHTML = '<option value="">Seleccione una locación</option>';
        locaciones.forEach(loc => {
            const option = document.createElement('option');
            option.value = loc.id_locacion;
            option.textContent = loc.nombre;
            select.appendChild(option);
        });
        
        console.log(`Select de locaciones actualizado con ${locaciones.length} opciones`);
    }
};

// ========== API ==========

const API = {
    async request(url, options = {}) {
        try {
            console.log(`Realizando petición ${options.method || 'GET'} a ${url}`);
            
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                credentials: 'same-origin',
                ...options
            });
            
            console.log(`Respuesta recibida: ${response.status} ${response.statusText}`);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error en la respuesta:', errorText);
                throw new Error(`Error ${response.status}: ${errorText}`);
            }
            
            const data = await response.json();
            console.log('Datos recibidos:', data);
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async getAll(entity) {
        const config = CONFIG.entities[entity];
        console.log(`Obteniendo todos los ${entity}s desde ${config.apiUrl}`);
        return await this.request(config.apiUrl);
    },
    
    async getById(entity, id) {
        const config = CONFIG.entities[entity];
        console.log(`Obteniendo ${entity} con ID ${id}`);
        return await this.request(`${config.apiUrl}/${id}`);
    },
    
    async create(entity, data) {
        const config = CONFIG.entities[entity];
        console.log(`Creando ${entity}:`, data);
        return await this.request(config.apiUrl, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async update(entity, id, data) {
        const config = CONFIG.entities[entity];
        console.log(`Actualizando ${entity} ${id}:`, data);
        return await this.request(`${config.apiUrl}/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    async delete(entity, id) {
        const config = CONFIG.entities[entity];
        console.log(`Eliminando ${entity} ${id}`);
        return await this.request(`${config.apiUrl}/${id}`, {
            method: 'DELETE'
        });
    }
};

// ========== GESTIÓN DE FORMULARIOS ==========

const FormManager = {
    getFormData(form) {
        const data = {};
        const fields = form.querySelectorAll('[data-field]');
        
        fields.forEach(field => {
            const fieldName = field.dataset.field;
            if (fieldName === 'id') return;
            
            let value = field.value;
            
            if (field.type === 'number') {
                if (value === '') {
                    if (field.hasAttribute('required')) {
                        return;
                    }
                    value = null;
                } else {
                    value = field.step === 'any' ? parseFloat(value) : parseInt(value);
                }
            }
            
            if (value !== '' && value !== null) {
                data[fieldName] = value;
            } else if (field.hasAttribute('required')) {
                console.warn(`Campo requerido vacío: ${fieldName}`);
            }
        });
        
        console.log('Datos extraídos del formulario:', data);
        return data;
    },
    
    setFormData(form, data) {
        console.log('Estableciendo datos en formulario:', data);
        
        if (!form) {
            console.error('Formulario no encontrado para setFormData');
            return;
        }
        
        const fields = form.querySelectorAll('[data-field]');
        
        fields.forEach(field => {
            const fieldName = field.dataset.field;
            if (fieldName === 'id' && data[CONFIG.entities[State.currentEntity].idField]) {
                field.value = data[CONFIG.entities[State.currentEntity].idField];
            } else if (data[fieldName] !== undefined && data[fieldName] !== null) {
                field.value = data[fieldName];
            }
        });
    },
    
    resetForm(form) {
        form.reset();
        const idField = form.querySelector('[data-field="id"]');
        if (idField) idField.value = '';
    }
};

// ========== GESTIÓN DE MODALES ==========

const ModalManager = {
    open(modalName, title = null) {
        // Cambia esto:
        // const modal = DOM.getByData('modal', modalName);
        
        // Por esto:
        const modal = document.getElementById(`modal-${modalName}`);
        
        if (!modal) {
            console.error(`Modal modal-${modalName} no encontrado`);
            return;
        }
        
        modal.classList.add('show');
        
        if (title) {
            const titleElement = modal.querySelector('[data-target="modal-title"]');
            if (titleElement) titleElement.textContent = title;
        }
        
        console.log(`Modal ${modalName} abierto`);
    },
    
    close(modalName) {
        const modal = document.getElementById(`modal-${modalName}`);
        if (!modal) return;
        
        modal.classList.remove('show');
        
        const form = modal.querySelector('form');
        if (form) FormManager.resetForm(form);
        
        console.log(`Modal ${modalName} cerrado`);
    }
};

// ========== NOTIFICACIONES ==========

const Notifier = {
    show(message, type = 'success') {
        console.log(`Mostrando notificación ${type}:`, message);
        
        const oldNotifications = document.querySelectorAll('.notification');
        oldNotifications.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.remove(), 3000);
    }
};

// ========== DASHBOARD ==========

const Dashboard = {
    chartCostos: null,
    chartEstatus: null,
    
    async loadDashboard() {
        try {
            console.log('Cargando estadísticas del dashboard...');
            const response = await API.request('/api/dashboard/estadisticas');
            
            this.updateSummary(response);
            this.renderChartCostos(response.rangos_costo);
            this.renderChartEstatus(response.estatus);
            
            console.log('Dashboard cargado correctamente');
        } catch (error) {
            console.error('Error al cargar dashboard:', error);
            Notifier.show('Error al cargar estadísticas', 'error');
        }
    },
    
    updateSummary(data) {
        document.getElementById('totalCasas').textContent = data.total_casas;
        document.getElementById('enVenta').textContent = data.en_venta;
        document.getElementById('vendidas').textContent = data.vendidas;
        
        const precioFormateado = new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN',
            minimumFractionDigits: 0
        }).format(data.precio_promedio);
        
        document.getElementById('precioPromedio').textContent = precioFormateado;
    },
    
    renderChartCostos(rangos) {
        const ctx = document.getElementById('chartCostos');
        
        if (this.chartCostos) {
            this.chartCostos.destroy();
        }
        
        this.chartCostos = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(rangos),
                datasets: [{
                    label: 'Cantidad de Casas',
                    data: Object.values(rangos),
                    backgroundColor: [
                        'rgba(42, 159, 214, 0.8)',
                        'rgba(19, 69, 99, 0.8)',
                        'rgba(127, 200, 66, 0.8)',
                        'rgba(243, 156, 18, 0.8)'
                    ],
                    borderColor: [
                        'rgba(42, 159, 214, 1)',
                        'rgba(19, 69, 99, 1)',
                        'rgba(127, 200, 66, 1)',
                        'rgba(243, 156, 18, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    },
    
    renderChartEstatus(estatus) {
        const ctx = document.getElementById('chartEstatus');
        
        if (this.chartEstatus) {
            this.chartEstatus.destroy();
        }
        
        this.chartEstatus = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['En Venta', 'Vendida'],
                datasets: [{
                    data: [estatus['En Venta'], estatus['Vendida']],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                size: 14
                            }
                        }
                    }
                }
            }
        });
    }
};

// ========== CONTROLADORES ==========

const Controller = {
    async loadTab(tabName) {
        console.log(`Cargando tab: ${tabName}`);
        State.currentTab = tabName;
        
        DOM.queryAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        const activeTab = DOM.getByData('tab', tabName);
        if (activeTab) activeTab.classList.add('active');
        
        DOM.queryAll('.tab-content').forEach(content => content.classList.remove('active'));
        const activeContent = DOM.query(`#${tabName}-tab`);
        if (activeContent) activeContent.classList.add('active');
        
        if (tabName === 'dashboard') {
            await Dashboard.loadDashboard();
        } else {
            await this.loadData(tabName);
        }
    },
    
    async loadData(entity) {
        try {
            console.log(`Cargando datos de ${entity}`);
            const items = await API.getAll(entity);
            Renderer.renderList(entity, items);
            
            if (entity === 'casa') {
                const locaciones = await API.getAll('locacion');
                Renderer.renderLocacionSelect(locaciones);
            }
        } catch (error) {
            console.error(`Error al cargar ${entity}:`, error);
            Notifier.show(`Error al cargar ${entity}: ${error.message}`, 'error');
        }
    },
    
    async openCreateModal(entity) {
        console.log(`Abriendo modal de creación para ${entity}`);
        const config = CONFIG.entities[entity];
        State.currentEntity = entity;
        State.currentId = null;
        
        if (entity === 'casa') {
            try {
                const locaciones = await API.getAll('locacion');
                Renderer.renderLocacionSelect(locaciones);
            } catch (error) {
                console.error('Error al cargar locaciones:', error);
            }
        }
        
        ModalManager.open(entity, config.titleNew);
    },
    
    async openEditModal(entity, id) {
        try {
            console.log(`Abriendo modal de edición para ${entity} ${id}`);
            const config = CONFIG.entities[entity];
            const data = await API.getById(entity, id);
            
            State.currentEntity = entity;
            State.currentId = id;
            
            if (entity === 'casa') {
                const locaciones = await API.getAll('locacion');
                Renderer.renderLocacionSelect(locaciones);
            }
            
            // Buscar el modal usando el ID correcto
            const modal = document.getElementById(`modal-${entity}`);
            if (!modal) {
                console.error(`Modal modal-${entity} no encontrado`);
                return;
            }
            
            const form = modal.querySelector('form');
            if (!form) {
                console.error(`Formulario no encontrado en modal-${entity}`);
                return;
            }
            
            FormManager.setFormData(form, data);
            ModalManager.open(entity, config.titleEdit);
            
        } catch (error) {
            console.error(`Error al cargar ${entity}:`, error);
            Notifier.show(`Error al cargar ${entity}: ${error.message}`, 'error');
        }
    },
    
    async submitForm(form, entity) {
        try {
            console.log(`Enviando formulario de ${entity}`);
            const data = FormManager.getFormData(form);
            const id = State.currentId;
            
            console.log(`ID actual: ${id}`);
            console.log(`Datos a enviar:`, data);
            
            if (id) {
                console.log('Actualizando registro...');
                await API.update(entity, id, data);
                Notifier.show(`${entity} actualizado exitosamente`, 'success');
            } else {
                console.log('Creando nuevo registro...');
                await API.create(entity, data);
                Notifier.show(`${entity} creado exitosamente`, 'success');
            }
            
            ModalManager.close(entity);
            await this.loadData(entity);
        } catch (error) {
            console.error(`Error al guardar ${entity}:`, error);
            Notifier.show(`Error al guardar ${entity}: ${error.message}`, 'error');
        }
    },
    
    async deleteItem(entity, id) {
        console.log(`Intentando eliminar ${entity} con ID ${id}`);
        if (!confirm(`¿Estás seguro de eliminar este ${entity}?`)) return;
        
        try {
            await API.delete(entity, id);
            Notifier.show(`${entity} eliminado exitosamente`, 'success');
            await this.loadData(entity);
        } catch (error) {
            console.error(`Error al eliminar ${entity}:`, error);
            Notifier.show(`Error al eliminar ${entity}: ${error.message}`, 'error');
        }
    }
};

// ========== EVENT DELEGATION ==========

const EventHandler = {
    init() {
        console.log('Inicializando manejadores de eventos...');
        
        document.addEventListener('click', (e) => {
            const target = e.target.closest('[data-action]');
            if (!target) return;
            
            const action = target.dataset.action;
            const entity = target.dataset.entity;
            const modal = target.dataset.modal;
            const tab = target.dataset.tab;
            const id = target.dataset.id;
            
            console.log('Click detectado:', { action, entity, modal, tab, id });
            
            switch(action) {
                case 'load-tab':
                    if (tab) Controller.loadTab(tab);
                    break;
                case 'open-modal':
                    if (modal) Controller.openCreateModal(modal);
                    break;
                case 'close-modal':
                    if (modal) ModalManager.close(modal);
                    break;
                case 'edit':
                    if (entity && id) Controller.openEditModal(entity, id);
                    break;
                case 'delete':
                    if (entity && id) Controller.deleteItem(entity, id);
                    break;
                case 'generar-reporte':
                    ReporteManager.generarPDF();
                    break;
                default:
                    console.warn('Acción desconocida:', action);
            }
        });
        
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (!form.dataset.form) return;
            
            e.preventDefault();
            const entity = form.dataset.entity;
            console.log('Formulario enviado para:', entity);
            Controller.submitForm(form, entity);
        });
        
        console.log('Manejadores de eventos inicializados correctamente');
    }
};

// ========== GESTIÓN DE REPORTES ==========

const ReporteManager = {
    async generarPDF() {
        try {
            console.log('Generando reporte PDF...');
            Notifier.show('Generando reporte PDF...', 'info');
            
            // Abrir el PDF en una nueva pestaña
            window.open('/api/reporte/casas-pdf', '_blank');
            
            console.log('Reporte PDF generado correctamente');
            
            // Notificación de éxito después de un pequeño delay
            setTimeout(() => {
                Notifier.show('Reporte PDF generado exitosamente', 'success');
            }, 1000);
            
        } catch (error) {
            console.error('Error al generar reporte PDF:', error);
            Notifier.show('Error al generar el reporte PDF', 'error');
        }
    }
};

// ========== INICIALIZACIÓN ==========

document.addEventListener('DOMContentLoaded', () => {
    console.log('====================================');
    console.log('Inicializando panel de administración...');
    console.log('====================================');
    
    const tablaCasas = DOM.query('#tabla-casas');
    if (!tablaCasas) {
        console.error('No se encontró #tabla-casas. Este script solo debe ejecutarse en el panel de administración.');
        return;
    }
    
    const templates = ['template-casa-row', 'template-locacion-row', 'template-usuario-row'];
    templates.forEach(templateId => {
        const template = document.getElementById(templateId);
        if (!template) {
            console.error(`Template ${templateId} no encontrado`);
        } else {
            console.log(`✓ Template ${templateId} encontrado`);
        }
    });
    
    EventHandler.init();
    Controller.loadData('casa');
    
    console.log('====================================');
    console.log('Panel de administración inicializado correctamente');
    console.log('====================================');
});