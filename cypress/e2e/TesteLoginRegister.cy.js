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

describe('User flow', () => {
  before(() => {
    cy.deleteUsers(); 
  });

  it('deve criar um usuario e fazer login no site', () => {
    cy.criarUser(); 
    cy.logar();
    
    cy.contains('TestandoCypress4').should('be.visible');
  });
});