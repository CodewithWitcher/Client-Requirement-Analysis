/**
 * Project Storage Engine
 * Auto-saves client project profiles, calculator states, questionnaires, and checklists in LocalStorage.
 * Includes JSON project export and import functions.
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
      return data ? JSON.parse(data) : {};
    } catch (e) {
      console.error('Error reading LocalStorage:', e);
      return {};
    }
  },

  /**
   * Get active project ID
   */
  getActiveProjectId: function() {
    return localStorage.getItem(this.ACTIVE_KEY) || 'default_project';
  },

  /**
   * Set active project ID
   */
  setActiveProjectId: function(id) {
    localStorage.setItem(this.ACTIVE_KEY, id);
  },

  /**
   * Get data for a specific project
   */
  getProject: function(id) {
    const projects = this.getAllProjects();
    const activeId = id || this.getActiveProjectId();
    if (!projects[activeId]) {
      projects[activeId] = {
        id: activeId,
        clientName: 'Client Name',
        projectName: 'New Project Proposal',
        preparedBy: 'Your Agency Name',
        date: new Date().toISOString().split('T')[0],
        platform: 'Both',
        complexity: '1.0',
        discount: 0,
        gstRate: 18,
        calculators: {},
        questionnaires: {},
        checklists: {},
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
   * Export project as downloadable JSON backup file
   */
  exportJSON: function(projectId) {
    const project = this.getProject(projectId);
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(project, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `project_${slugifyStr(project.projectName)}_${project.date}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    if (window.showToast) window.showToast('Project configuration exported as JSON!', 'success');
  },

  /**
   * Import project from JSON file payload
   */
  importJSON: function(jsonString) {
    try {
      const project = JSON.parse(jsonString);
      if (!project.id || !project.projectName) {
        throw new Error('Invalid project JSON file structure.');
      }
      project.id = 'imported_' + Date.now();
      this.saveProject(project);
      this.setActiveProjectId(project.id);
      if (window.showToast) window.showToast(`Imported project: ${project.projectName}`, 'success');
      setTimeout(() => location.reload(), 800);
    } catch (e) {
      if (window.showToast) window.showToast(`Import failed: ${e.message}`, 'error');
    }
  }
};

function slugifyStr(str) {
  return (str || 'project').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
}
