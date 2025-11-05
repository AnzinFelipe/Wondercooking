Cypress.Commands.add('deleteUsers', () => {
  cy.exec('python delete_users.py', { 
    failOnNonZeroExit: false,
    timeout: 15000 
  }).then((result) => {
    cy.log('Exit code:', result.code);
    if (result.stdout) {
      cy.log('Cleanup result:', result.stdout);
    }
    if (result.stderr) {
      cy.log('Cleanup stderr:', result.stderr);
    }
  });
});

Cypress.Commands.add('criarUser', () => {
  cy.visit('http://127.0.0.1:8000/registrar/');
  
  cy.get('#username').should('be.visible');
  
  cy.get('#username').type('TestandoCypress4'); 
  cy.get('#email').type('testeCypress4@gmail.com'); 
  cy.get('#senha').type('12345678'); 
  cy.get('#senhaconfirmar').type('12345678'); 
  
  cy.get('button[type="submit"]').click();
  
  cy.url().should('not.include', '/registrar/');
});

Cypress.Commands.add('logar', () => {
  cy.visit('http://127.0.0.1:8000/accounts/login/');  
  cy.get('#username').type('TestandoCypress4'); 
  cy.get('#password').type('12345678');  
  cy.get('button[type="submit"]').click();  
    
  cy.url().should('not.include', '/login/');
});

Cypress.Commands.add('criarPostagem', () => {
  cy.visit('http://127.0.0.1:8000/criar_post/');

  cy.get('#titulo').should('be.visible');

  cy.get('#titulo').type('Testando Pesquisar Ingrediente');
  cy.get('#descricao').type('Testando descrição, Ingredientes: tomate, queijo');
  cy.get('#hashtags').type('#testando');
  cy.get('#imagem').selectFile('cypress/fixtures/imagem_teste.jpg', { force: true });

  cy.contains('button', 'Criar Postagem').click();
  cy.wait(2000);
  cy.url().should('not.include', '/criar_post/');
});

Cypress.Commands.add('pesquisarEVerificar', () => {
  cy.get('input[name="objeto"]').type('tomate');
  cy.get('form[action*="pesquisar_ingredientes"] button').click();
  cy.wait(2000);
  cy.contains('Testando Pesquisar Ingrediente').should('be.visible');
});

describe('User flow completo', () => {
  before(() => {
    cy.deleteUsers(); 
    cy.criarUser(); 
    cy.logar();
    cy.criarPostagem();
  });

  it('deve pesquisar e encontrar o título da postagem', () => {
    cy.pesquisarEVerificar();
  });
});