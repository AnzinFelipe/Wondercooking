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

Cypress.Commands.add('selecionarAlergiaOvoPerfil', () => {
  cy.contains('TestandoCypress4').click();
  cy.url().should('include', '/perfil/');
  cy.contains('label', 'Ovo').click();
  cy.contains('button', 'Salvar Alergias').click();
  cy.contains('a', 'Wondercooking').click();
});

Cypress.Commands.add('criarPostagemComOvo', () => {
  cy.visit('http://127.0.0.1:8000/criar_post/');

  cy.get('#titulo').should('be.visible');

  cy.get('#titulo').type('Testando titulo com Ovo');
  cy.get('#descricao').type('Testando descrição com ovo');
  cy.get('#hashtags').type('#ovo');
  cy.contains('label', 'Ovo').click();
  cy.get('#imagem').selectFile('cypress/fixtures/imagem_teste.jpg', { force: true });
  cy.get('button[type="submit"]').click();

  cy.url().should('not.include', '/criar_post/');
});

describe('User flow', () => {
  before(() => {
    cy.deleteUsers(); 
    cy.criarUser(); 
    cy.logar();
  });

  it('deve criar uma postagem e filtrar por alergia', () => {
    cy.selecionarAlergiaOvoPerfil();
    cy.criarPostagemComOvo();
    cy.contains('Testando titulo com Ovo').should('not.exist');
    cy.url().should('include', 'http://127.0.0.1:8000/');
  });
});