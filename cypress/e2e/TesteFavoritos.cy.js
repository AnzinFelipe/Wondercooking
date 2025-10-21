Cypress.Commands.add('deleteUsers', () => {
  cy.exec('python delete_users.py', { failOnNonZeroExit: false })
    .then((result) => {
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

Cypress.commands.add('criarPostagem', () => {
    cy.visit('http://127.0.0.1:8000/criar_post/');

    cy.get('#titulo').should('be.visible');

    cy.get('#titulo').type('Testando titulo');
    cy.get('#descricao').type('Testando descrição');
    cy.get('#hashtags').type('#testando');
    cy.get('#imagem').selectFile('cypress/fixtures/imagem_teste.jpg', { force: true });

    cy.get('button[type="submit"]').click();

    cy.url().should('not.include', '/criar_post/');
});

Cypress.Commands.add('verFavoritos', () => {
    cy.get('button').contains('☆ Favoritar').first().click();
    cy.contains('button', '★ Favoritado').should('exist');

    cy.visit('http://127.0.0.1:8000/favoritos/');
});

describe('User flow', () => {
  before(() => {
    cy.deleteUsers(); 
    cy.criarUser(); 
    cy.logar();
    cy.criarPostagem();
  });

  it('', () => {
    cy.verFavoritos();

    cy.contains('Testando titulo').should('be.visible');
  });
});