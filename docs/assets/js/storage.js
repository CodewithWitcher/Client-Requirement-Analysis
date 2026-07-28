/**
 * Project & Multi-Client Storage Engine
 * Auto-saves client project profiles, calculator states, questionnaires, task checklists, and live document edits in LocalStorage.
 * Includes multi-client profile management, warning banners, JSON backups, and workspace exports.
 */

window.ProjectStorage = {
  STORAGE_KEY: 'client_req_projects_db',
  ACTIVE_KEY: 'client_req_active_id',

  /**
   * Fetch all saved project records
   */
  getAllProjects: function() {
    try {
      const data = localStorage.getItem(this.STORAGE_KEY);
      const obj = data ? JSON.parse(data) : {};
      if (!Object.keys(obj).length) {
        // Create default initial client profile
        const defaultId = 'client_default';
        obj[defaultId] = {
          id: defaultId,
          clientName: 'Acme Corporation',
          projectName: 'Website & App Solution',
          preparedBy: 'Agency Team',
          date: new Date().toISOString().split('T')[0],
          platform: 'Both',
          complexity: '1.0',
          discount: 0,
          gstRate: 18,
          calculators: {},
          questionnaires: {},
          checklists: {},
          editedDocs: {},
          checkedItems: {},
          updatedAt: new Date().toISOString()
        };
        this.saveProjects(obj);
      }
      return obj;
    } catch (e) {
      console.error('Error reading LocalStorage:', e);
      return {};
    }
  },

  /**
   * Get active project ID
   */
  getActiveProjectId: function() {
    return localStorage.getItem(this.ACTIVE_KEY) || 'client_default';
  },

  /**
   * Set active project ID
   */
  setActiveProjectId: function(id) {
    localStorage.setItem(this.ACTIVE_KEY, id);
  },

  /**
   * Get data for active project profile
   */
  getProject: function(id) {
    const projects = this.getAllProjects();
    const activeId = id || this.getActiveProjectId();
    if (!projects[activeId]) {
      projects[activeId] = {
        id: activeId,
        clientName: 'New Client',
        projectName: 'Requirement Scope & Pricing',
        preparedBy: 'Agency Team',
        date: new Date().toISOString().split('T')[0],
        platform: 'Both',
        complexity: '1.0',
        discount: 0,
        gstRate: 18,
        calculators: {},
        questionnaires: {},
        checklists: {},
        editedDocs: {},
        checkedItems: {},
        updatedAt: new Date().toISOString()
      };
      this.saveProjects(projects);
    }
    return projects[activeId];
  },

  /**
   * Save a single project
   */
  saveProject: function(projectData) {
    const projects = this.getAllProjects();
    projectData.updatedAt = new Date().toISOString();
    projects[projectData.id] = projectData;
    this.saveProjects(projects);
  },

  /**
   * Save full projects dictionary
   */
  saveProjects: function(projects) {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(projects));
    } catch (e) {
      console.error('Failed saving to LocalStorage:', e);
    }
  },

  /**
   * Create new Client Profile
   */
  createClientProfile: function(clientName, projectName) {
    const projects = this.getAllProjects();
    const newId = 'client_' + Date.now();
    projects[newId] = {
      id: newId,
      clientName: clientName || 'New Client',
      projectName: projectName || 'Client Project Scope',
      preparedBy: 'Agency Team',
      date: new Date().toISOString().split('T')[0],
      platform: 'Both',
      complexity: '1.0',
      discount: 0,
      gstRate: 18,
      calculators: {},
      questionnaires: {},
      checklists: {},
      editedDocs: {},
      checkedItems: {},
      updatedAt: new Date().toISOString()
    };
    this.saveProjects(projects);
    this.setActiveProjectId(newId);
    return projects[newId];
  },

  /**
   * Delete Client Profile
   */
  deleteClientProfile: function(id) {
    const projects = this.getAllProjects();
    if (Object.keys(projects).length <= 1) {
      if (window.showToast) window.showToast('Cannot delete the last remaining client profile.', 'warning');
      return false;
    }

    delete projects[id];
    this.saveProjects(projects);
    
    // Switch to first remaining client
    const nextId = Object.keys(projects)[0];
    this.setActiveProjectId(nextId);
    return true;
  },

  /**
   * Export project as downloadable JSON backup file
   */
  exportJSON: function(projectId) {
    const project = this.getProject(projectId);
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(project, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `client_${slugifyStr(project.clientName)}_${project.date}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    if (window.showToast) window.showToast('Client project configuration exported as JSON!', 'success');
  },

  /**
   * Import project from JSON file payload
   */
  importJSON: function(jsonString) {
    try {
      const project = JSON.parse(jsonString);
      if (!project.id || !project.clientName) {
        throw new Error('Invalid client project JSON file structure.');
      }
      project.id = 'imported_' + Date.now();
      this.saveProject(project);
      this.setActiveProjectId(project.id);
      if (window.showToast) window.showToast(`Imported profile: ${project.clientName}`, 'success');
      setTimeout(() => location.reload(), 800);
    } catch (e) {
      if (window.showToast) window.showToast(`Import failed: ${e.message}`, 'error');
    }
  }
};

function slugifyStr(str) {
  return (str || 'project').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
}
